package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"io"
	"math/rand"
	"net/http"
	"os"
	"sort"
	"strings"
	"time"

	"github.com/Exonymos/pokedexcli/internal/pokecache"
)

// Config struct to hold app state
type Config struct {
	PokeapiClient       http.Client
	NextLocationAreaURL *string
	PrevLocationAreaURL *string
	UserPokedex         map[string]PokemonApiResponse // For caught Pokemon
	Cache               *pokecache.Cache
}

// Struct to represent the JSON response for location areas
type LocationAreaResponse struct {
	Count    int     `json:"count"`
	Next     *string `json:"next"`
	Previous *string `json:"previous"`
	Results  []struct {
		Name string `json:"name"`
		URL  string `json:"url"`
	} `json:"results"`
}

// Struct to represent the JSON response for location area details
type LocationAreaDetailResponse struct {
	Name              string `json:"name"`
	PokemonEncounters []struct {
		Pokemon struct {
			Name string `json:"name"`
			URL  string `json:"url"`
		} `json:"pokemon"`
	} `json:"pokemon_encounters"`
}

// Struct to represent the JSON response for Pokemon details
type PokemonApiResponse struct {
	ID             int    `json:"id"`
	Name           string `json:"name"`
	BaseExperience int    `json:"base_experience"`
	Height         int    `json:"height"`
	Weight         int    `json:"weight"`
	Stats          []struct {
		BaseStat int `json:"base_stat"`
		Stat     struct {
			Name string `json:"name"`
			URL  string `json:"url"` // URL of the stat
		} `json:"stat"`
	} `json:"stats"`
	Types []struct {
		Slot int `json:"slot"`
		Type struct {
			Name string `json:"name"`
			URL  string `json:"url"` // URL of the type
		} `json:"type"`
	} `json:"types"`
}

// cliCommand struct definition
type cliCommand struct {
	name        string
	description string
	callback    func(*Config, ...string) error
}

// getCommands returns a map of available CLI commands
func getCommands() map[string]cliCommand {
	return map[string]cliCommand{
		"help": {
			name:        "help",
			description: "Displays a help message",
			callback:    commandHelp,
		},
		"exit": {
			name:        "exit",
			description: "Exit the Pokedex",
			callback:    commandExit,
		},
		"map": {
			name:        "map",
			description: "Displays the next 20 location areas",
			callback:    commandMap,
		},
		"mapb": {
			name:        "mapb",
			description: "Displays the previous 20 location areas",
			callback:    commandMapb,
		},
		"explore": {
			name:        "explore <location_area_name>",
			description: "Lists Pokemon in a specific location area",
			callback:    commandExplore,
		},
		"catch": {
			name:        "catch <pokemon_name>",
			description: "Attempt to catch a Pokemon",
			callback:    commandCatch,
		},
		"inspect": {
			name:        "inspect <pokemon_name>",
			description: "View details of a caught Pokemon",
			callback:    commandInspect,
		},
	}
}

// callback for the "exit" command
func commandExit(_ *Config, _ ...string) error {
	fmt.Println("Closing the Pokedex... Goodbye!")
	os.Exit(0)
	return nil
}

// callback for the "help" command
func commandHelp(_ *Config, _ ...string) error {
	fmt.Println("\nWelcome to the Pokedex!")
	fmt.Println("Usage:")
	fmt.Println("")

	availableCommands := getCommands()

	// Sort command names for consistent output
	var commandNames []string
	for name := range availableCommands {
		commandNames = append(commandNames, name)
	}
	sort.Strings(commandNames)
	for _, name := range commandNames {
		cmd := availableCommands[name]
		fmt.Printf("%s: %s\n", cmd.name, cmd.description)
	}

	fmt.Println("")
	return nil
}

// callback for the "map" command
func commandMap(cfg *Config, _ ...string) error {
	urlToFetch := "https://pokeapi.co/api/v2/location-area/"
	if cfg.NextLocationAreaURL != nil && *cfg.NextLocationAreaURL != "" {
		urlToFetch = *cfg.NextLocationAreaURL
	}

	fmt.Printf("Fetching location areas from: %s\n", urlToFetch) // Debugging line

	var body []byte
	var err error

	// Try to get from cache first
	cachedData, found := cfg.Cache.Get(urlToFetch)
	if found {
		fmt.Println("(Cache hit for location areas)")
		body = cachedData
	} else {
		fmt.Println("(Cache miss for location areas, fetching...)")
		resp, errHttp := cfg.PokeapiClient.Get(urlToFetch)
		if errHttp != nil {
			return fmt.Errorf("failed to fetch location areas: %w", errHttp)
		}
		defer resp.Body.Close()

		if resp.StatusCode > 299 {
			bodyBytes, _ := io.ReadAll(resp.Body)
			return fmt.Errorf("bad status code: %d from %s. Response: %s", resp.StatusCode, urlToFetch, string(bodyBytes))
		}

		body, err = io.ReadAll(resp.Body)
		if err != nil {
			return fmt.Errorf("failed to read response body: %w", err)
		}
		// Add to cache
		cfg.Cache.Add(urlToFetch, body)
	}

	var locationAreasResp LocationAreaResponse
	err = json.Unmarshal(body, &locationAreasResp)
	if err != nil {
		return fmt.Errorf("failed to unmarshal JSON response: %w (Body: %s)", err, string(body))
	}

	fmt.Println("Location Areas:")
	for _, area := range locationAreasResp.Results {
		fmt.Println(area.Name)
	}

	cfg.NextLocationAreaURL = locationAreasResp.Next
	cfg.PrevLocationAreaURL = locationAreasResp.Previous

	return nil
}

// callback for the "mapb" (map back) command
func commandMapb(cfg *Config, _ ...string) error {
	if cfg.PrevLocationAreaURL == nil || *cfg.PrevLocationAreaURL == "" {
		fmt.Println("You're on the first page, cannot go back further.")
		return nil
	}

	urlToFetch := *cfg.PrevLocationAreaURL
	fmt.Printf("Fetching previous location areas from: %s\n", urlToFetch) // Debugging line

	var body []byte
	var err error

	cachedData, found := cfg.Cache.Get(urlToFetch)
	if found {
		fmt.Println("(Cache hit for previous location areas)")
		body = cachedData
	} else {
		fmt.Println("(Cache miss for previous location areas, fetching...)")
		resp, errHttp := cfg.PokeapiClient.Get(urlToFetch)
		if errHttp != nil {
			return fmt.Errorf("failed to fetch previous location areas: %w", errHttp)
		}
		defer resp.Body.Close()

		if resp.StatusCode > 299 {
			bodyBytes, _ := io.ReadAll(resp.Body)
			return fmt.Errorf("bad status code: %d from %s. Response: %s", resp.StatusCode, urlToFetch, string(bodyBytes))
		}

		body, err = io.ReadAll(resp.Body)
		if err != nil {
			return fmt.Errorf("failed to read response body: %w", err)
		}
		cfg.Cache.Add(urlToFetch, body)
	}

	var locationAreasResp LocationAreaResponse
	err = json.Unmarshal(body, &locationAreasResp)
	if err != nil {
		return fmt.Errorf("failed to unmarshal JSON response: %w (Body: %s)", err, string(body))
	}

	fmt.Println("Location Areas (Previous):")
	for _, area := range locationAreasResp.Results {
		fmt.Println(area.Name)
	}

	cfg.NextLocationAreaURL = locationAreasResp.Next
	cfg.PrevLocationAreaURL = locationAreasResp.Previous

	return nil
}

// callback for the "explore" command
func commandExplore(cfg *Config, args ...string) error {
	if len(args) == 0 {
		return fmt.Errorf("please specify a location area name to explore")
	}
	locationAreaName := args[0]
	fmt.Printf("Exploring %s...\n", locationAreaName)

	urlToFetch := fmt.Sprintf("https://pokeapi.co/api/v2/location-area/%s/", locationAreaName)

	var body []byte
	var err error

	cachedData, found := cfg.Cache.Get(urlToFetch)
	if found {
		fmt.Printf("(Cache hit for %s details)\n", locationAreaName)
		body = cachedData
	} else {
		fmt.Printf("(Cache miss for %s details, fetching...)\n", locationAreaName)
		resp, errHttp := cfg.PokeapiClient.Get(urlToFetch)
		if errHttp != nil {
			return fmt.Errorf("failed to fetch details for %s: %w", locationAreaName, errHttp)
		}
		defer resp.Body.Close()

		if resp.StatusCode > 299 {
			bodyBytes, _ := io.ReadAll(resp.Body)
			return fmt.Errorf("bad status code: %d from %s. Response: %s", resp.StatusCode, urlToFetch, string(bodyBytes))
		}

		body, err = io.ReadAll(resp.Body)
		if err != nil {
			return fmt.Errorf("failed to read response body for %s: %w", locationAreaName, err)
		}
		cfg.Cache.Add(urlToFetch, body)
	}

	var areaDetailResp LocationAreaDetailResponse
	err = json.Unmarshal(body, &areaDetailResp)
	if err != nil {
		return fmt.Errorf("failed to unmarshal JSON for %s: %w (Body: %s)", locationAreaName, err, string(body))
	}

	if len(areaDetailResp.PokemonEncounters) == 0 {
		fmt.Printf("No Pokemon found in %s.\n", locationAreaName)
		return nil
	}

	fmt.Println("Found Pokemon:")
	for _, encounter := range areaDetailResp.PokemonEncounters {
		fmt.Printf(" - %s\n", encounter.Pokemon.Name)
	}
	return nil
}

// callback for the "catch" command
func commandCatch(cfg *Config, args ...string) error {
	if len(args) == 0 {
		return fmt.Errorf("please specify a Pokemon name to catch")
	}
	pokemonName := args[0]
	fmt.Printf("Throwing a Pokeball at %s...\n", pokemonName)

	urlToFetch := fmt.Sprintf("https://pokeapi.co/api/v2/pokemon/%s/", pokemonName)

	var body []byte
	var err error

	cachedData, found := cfg.Cache.Get(urlToFetch)
	if found {
		fmt.Printf("(Cache hit for %s data)\n", pokemonName)
		body = cachedData
	} else {
		fmt.Printf("(Cache miss for %s data, fetching...)\n", pokemonName)
		resp, errHttp := cfg.PokeapiClient.Get(urlToFetch)
		if errHttp != nil {
			return fmt.Errorf("failed to fetch details for %s: %w", pokemonName, errHttp)
		}
		defer resp.Body.Close()

		if resp.StatusCode == http.StatusNotFound {
			fmt.Printf("Pokemon '%s' not found.\n", pokemonName)
			return nil
		}
		if resp.StatusCode > 299 {
			bodyBytes, _ := io.ReadAll(resp.Body)
			return fmt.Errorf("bad status code: %d from %s. Response: %s", resp.StatusCode, urlToFetch, string(bodyBytes))
		}

		body, err = io.ReadAll(resp.Body)
		if err != nil {
			return fmt.Errorf("failed to read response body for %s: %w", pokemonName, err)
		}
		cfg.Cache.Add(urlToFetch, body)
	}

	var pokemonData PokemonApiResponse
	err = json.Unmarshal(body, &pokemonData)
	if err != nil {
		return fmt.Errorf("failed to unmarshal JSON for %s: %w (Body: %s)", pokemonName, err, string(body))
	}

	// Simulate a catch attempt
	const catchThreshold = 60 // Adjust to increase/decrease catch difficulty
	roll := rand.Intn(pokemonData.BaseExperience + catchThreshold)

	if roll < catchThreshold {
		fmt.Printf("%s was caught!\n", pokemonName)
		cfg.UserPokedex[pokemonName] = pokemonData // Store in Pokedex
		fmt.Printf("Added %s to your Pokedex.\n", pokemonName)
	} else {
		fmt.Printf("%s escaped!\n", pokemonName)
	}
	return nil
}

// callback for the "inspect" command
func commandInspect(cfg *Config, args ...string) error {
	if len(args) == 0 {
		return fmt.Errorf("please specify a Pokemon name to inspect")
	}
	pokemonName := args[0]

	pokemonData, caught := cfg.UserPokedex[pokemonName]
	if !caught {
		fmt.Printf("You have not caught '%s' yet.\n", pokemonName)
		return nil
	}

	fmt.Printf("Name: %s\n", pokemonData.Name)
	fmt.Printf("Height: %d\n", pokemonData.Height)
	fmt.Printf("Weight: %d\n", pokemonData.Weight)
	fmt.Println("Stats:")
	for _, stat := range pokemonData.Stats {
		fmt.Printf("  -%s: %d\n", stat.Stat.Name, stat.BaseStat)
	}
	fmt.Println("Types:")
	for _, typ := range pokemonData.Types {
		fmt.Printf("  - %s\n", typ.Type.Name)
	}
	return nil
}

func cleanInput(text string) []string {
	output := strings.ToLower(text)
	output = strings.TrimSpace(output)
	words := strings.Fields(output)
	if len(words) == 0 {
		return []string{}
	}
	return words
}

func startRepl(cfg *Config) {
	scanner := bufio.NewScanner(os.Stdin)
	availableCommands := getCommands()

	for {
		fmt.Print("Pokedex > ")

		scanned := scanner.Scan()
		if !scanned {
			if err := scanner.Err(); err != nil {
				fmt.Fprintln(os.Stderr, "Error reading input:", err)
			}
			fmt.Println("\nExiting Pokedex due to input error or EOF.")
			return
		}

		userInput := scanner.Text()
		cleanedWords := cleanInput(userInput)

		if len(cleanedWords) == 0 {
			continue
		}

		commandName := cleanedWords[0]
		var args []string
		if len(cleanedWords) > 1 {
			args = cleanedWords[1:]
		}

		command, exists := availableCommands[commandName]
		if exists {
			err := command.callback(cfg, args...)

			if err != nil {
				fmt.Fprintln(os.Stderr, "Error executing command:", err)
			}
		} else {
			fmt.Println("Unknown command. Type 'help' for available commands.")
		}
	}
}

func main() {
	// Seed the random number generator
	rand.Seed(time.Now().UnixNano())

	const cacheReapInterval = 5 * time.Minute // How often to reap, and max age of entries
	pokeCache := pokecache.NewCache(cacheReapInterval)

	// Initialize the config
	initialNextURL := "https://pokeapi.co/api/v2/location-area/"

	cfg := Config{
		PokeapiClient: http.Client{
			Timeout: 10 * time.Second,
		},
		NextLocationAreaURL: &initialNextURL,
		PrevLocationAreaURL: nil,
		UserPokedex:         make(map[string]PokemonApiResponse),
		Cache:               pokeCache,
	}
	startRepl(&cfg)
}
