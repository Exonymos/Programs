package main

import (
	"bufio"
	"encoding/gob"
	"errors"
	"fmt"
	"math/rand"
	"os"
	"sort"
	"strings"
	"time"

	"github.com/Exonymos/pokedexcli/internal/pokeapi"
	"github.com/Exonymos/pokedexcli/internal/pokecache"
)

// Config struct to hold app state
type Config struct {
	PokeAPIClient       pokeapi.APIClient
	NextLocationAreaURL *string
	PrevLocationAreaURL *string
	UserPokedex         map[string]pokeapi.PokemonApiResponse // For caught Pokemon
}

// Struct to represent the application state
type AppState struct {
	UserPokedex         map[string]pokeapi.PokemonApiResponse
	NextLocationAreaURL *string
	PrevLocationAreaURL *string
}

// cliCommand struct definition
type cliCommand struct {
	name        string
	description string
	callback    func(*Config, ...string) error
}

const saveFilePath = "pokedex.gob"

// Save the app state to a file
func saveAppState(cfg *Config) error {
	state := AppState{
		UserPokedex:         cfg.UserPokedex,
		NextLocationAreaURL: cfg.NextLocationAreaURL,
		PrevLocationAreaURL: cfg.PrevLocationAreaURL,
	}

	file, err := os.Create(saveFilePath)
	if err != nil {
		return fmt.Errorf("could not create save file '%s': %w", saveFilePath, err)
	}
	defer file.Close()

	encoder := gob.NewEncoder(file)
	err = encoder.Encode(state)
	if err != nil {
		return fmt.Errorf("could not encode app state to save file '%s': %w", saveFilePath, err)
	}

	return nil
}

// Load the app state from a file
func loadAppState() (*AppState, error) {
	file, err := os.Open(saveFilePath)
	if err != nil {
		if os.IsNotExist(err) {
			return nil, nil
		}
		return nil, fmt.Errorf("could not open save file '%s': %w", saveFilePath, err)
	}
	defer file.Close()

	var state AppState
	decoder := gob.NewDecoder(file)
	err = decoder.Decode(&state)
	if err != nil {
		return nil, fmt.Errorf("could not decode app state from save file '%s': %w", saveFilePath, err)
	}
	fmt.Println("Progress loaded!")
	return &state, nil
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
		"pokedex": {
			name:        "pokedex",
			description: "Lists all Pokemon you have caught",
			callback:    commandPokedex,
		},
	}
}

// callback for the "exit" command
func commandExit(cfg *Config, _ ...string) error {
	fmt.Println("Saving progress...")
	err := saveAppState(cfg)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error saving progress: %v\n", err)
	} else {
		fmt.Println("Progress saved successfully to", saveFilePath)
	}

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
	fmt.Printf("Fetching next location areas...\n")
	if cfg.NextLocationAreaURL != nil && *cfg.NextLocationAreaURL != "" {
		fmt.Printf("(from: %s)\n", *cfg.NextLocationAreaURL)
	}

	locationAreasResp, err := cfg.PokeAPIClient.ListLocationAreas(cfg.NextLocationAreaURL)
	if err != nil {
		return fmt.Errorf("could not get location areas: %w", err)
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

	fmt.Printf("Fetching previous location areas from: %s\n", *cfg.PrevLocationAreaURL) // Debugging line

	locationAreasResp, err := cfg.PokeAPIClient.ListLocationAreas(cfg.PrevLocationAreaURL)
	if err != nil {
		return fmt.Errorf("could not get previous location areas: %w", err)
	}

	fmt.Println("Location Areas (Previous):")
	for _, area := range locationAreasResp.Results {
		fmt.Println(area.Name)
	}

	cfg.NextLocationAreaURL = locationAreasResp.Next
	cfg.PrevLocationAreaURL = locationAreasResp.Previous

	return nil
}

const randomEncounterChance = 0.30

// callback for the "explore" command
func commandExplore(cfg *Config, args ...string) error {
	if len(args) == 0 {
		return fmt.Errorf("please specify a location area name to explore")
	}
	locationAreaName := args[0]
	fmt.Printf("Exploring %s...\n", locationAreaName)

	areaDetailResp, err := cfg.PokeAPIClient.GetLocationAreaDetail(locationAreaName)
	if err != nil {
		if errors.Is(err, pokeapi.ErrResourceNotFound) {
			fmt.Printf("Location area '%s' not found.\n", locationAreaName)
			return nil
		}
		return fmt.Errorf("could not get details for %s: %w", locationAreaName, err)
	}

	if len(areaDetailResp.PokemonEncounters) == 0 {
		fmt.Printf("No Pokemon found in %s.\n", locationAreaName)
		return nil
	}

	fmt.Println("Found Pokemon:")
	for _, encounter := range areaDetailResp.PokemonEncounters {
		fmt.Printf(" - %s\n", encounter.Pokemon.Name)
	}

	if rand.Float64() < randomEncounterChance {
		randomIndex := rand.Intn(len(areaDetailResp.PokemonEncounters))
		encounteredPokemon := areaDetailResp.PokemonEncounters[randomIndex].Pokemon

		fmt.Printf("❗ A wild %s has appeared! ❗\n", strings.Title(encounteredPokemon.Name))
		fmt.Printf("Quick! Try to `catch %s` before it gets away!\n\n", encounteredPokemon.Name)
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

	pokemonData, err := cfg.PokeAPIClient.GetPokemonInfo(pokemonName)
	if err != nil {
		if errors.Is(err, pokeapi.ErrResourceNotFound) {
			fmt.Printf("Pokemon '%s' not found by API.\n", pokemonName)
			return nil
		}
		return fmt.Errorf("could not get info for %s: %w", pokemonName, err)
	}

	// Simulate a catch attempt
	const catchThreshold = 60 // Adjust to increase/decrease catch difficulty
	roll := rand.Intn(pokemonData.BaseExperience + catchThreshold)

	if roll < catchThreshold {
		fmt.Printf("%s was caught!\n", pokemonName)
		cfg.UserPokedex[pokemonName] = pokemonData // Store in Pokedex
		fmt.Printf("You may now inspect %s using the 'inspect' command.\n", pokemonName)
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

// callback for the "pokedex" command
func commandPokedex(cfg *Config, _ ...string) error {
	if len(cfg.UserPokedex) == 0 {
		fmt.Println("Your Pokedex is empty. Go catch some Pokemon!")
		return nil
	}

	fmt.Println("Your Pokedex:")
	// To print in a consistent (sorted) order
	var caughtPokemonNames []string
	for name := range cfg.UserPokedex {
		caughtPokemonNames = append(caughtPokemonNames, name)
	}
	sort.Strings(caughtPokemonNames)

	for _, name := range caughtPokemonNames {
		fmt.Printf(" - %s\n", name)
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

	// Initialize PokeAPI Client
	const httpClientTimeout = 10 * time.Second
	apiClient := pokeapi.NewClient(pokeCache, httpClientTimeout)

	// Initialize the config
	initialNextURLStr := pokeapi.BaseURL + "/location-area/"
	cfg := Config{
		PokeAPIClient:       &apiClient,
		UserPokedex:         make(map[string]pokeapi.PokemonApiResponse),
		NextLocationAreaURL: &initialNextURLStr,
		PrevLocationAreaURL: nil,
	}

	loadedState, loadErr := loadAppState()
	if loadErr != nil {
		if !os.IsNotExist(loadErr) {
			fmt.Fprintf(os.Stderr, "Warning: could not load saved progress: %v\n", loadErr)
		}
		fmt.Println("Starting new Pokedex session (no valid save file found or error during load)...")
	} else if loadedState != nil {
		fmt.Println("Resuming from saved progress...")
		if loadedState.UserPokedex != nil {
			cfg.UserPokedex = loadedState.UserPokedex
		}
		if loadedState.NextLocationAreaURL != nil || loadedState.PrevLocationAreaURL != nil {
			cfg.NextLocationAreaURL = loadedState.NextLocationAreaURL
			cfg.PrevLocationAreaURL = loadedState.PrevLocationAreaURL
		}
		if cfg.NextLocationAreaURL == nil && cfg.PrevLocationAreaURL == nil {
			cfg.NextLocationAreaURL = &initialNextURLStr
		}
	} else {
		fmt.Println("Starting new Pokedex session (no save file found)...")
	}

	startRepl(&cfg)
}
