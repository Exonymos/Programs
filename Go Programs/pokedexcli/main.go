package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"sort"
	"strings"
	"time"
)

// Config struct to hold app state
type Config struct {
	PokeapiClient       http.Client
	NextLocationAreaURL *string
	PrevLocationAreaURL *string
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

// cliCommand struct definition
type cliCommand struct {
	name        string
	description string
	callback    func(*Config) error
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
	}
}

// callback for the "exit" command
func commandExit(_ *Config) error {
	fmt.Println("Closing the Pokedex... Goodbye!")
	os.Exit(0)
	return nil
}

// callback for the "help" command
func commandHelp(_ *Config) error {
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
func commandMap(cfg *Config) error {
	urlToFetch := "https://pokeapi.co/api/v2/location-area/"
	if cfg.NextLocationAreaURL != nil && *cfg.NextLocationAreaURL != "" {
		urlToFetch = *cfg.NextLocationAreaURL
	}

	fmt.Printf("Fetching location areas from: %s\n", urlToFetch) // Debugging line

	resp, err := cfg.PokeapiClient.Get(urlToFetch)
	if err != nil {
		return fmt.Errorf("failed to fetch location areas: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode > 299 {
		return fmt.Errorf("bad status code: %d from %s", resp.StatusCode, urlToFetch)
	}

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return fmt.Errorf("failed to read response body: %w", err)
	}

	var locationAreasResp LocationAreaResponse
	err = json.Unmarshal(body, &locationAreasResp)
	if err != nil {
		return fmt.Errorf("failed to unmarshal JSON response: %w", err)
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
func commandMapb(cfg *Config) error {
	if cfg.PrevLocationAreaURL == nil || *cfg.PrevLocationAreaURL == "" {
		fmt.Println("You're on the first page, cannot go back further.")
		return nil
	}

	urlToFetch := *cfg.PrevLocationAreaURL
	fmt.Printf("Fetching previous location areas from: %s\n", urlToFetch) // Debugging line

	resp, err := cfg.PokeapiClient.Get(urlToFetch)
	if err != nil {
		return fmt.Errorf("failed to fetch previous location areas: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode > 299 {
		return fmt.Errorf("bad status code: %d from %s", resp.StatusCode, urlToFetch)
	}

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return fmt.Errorf("failed to read response body: %w", err)
	}

	var locationAreasResp LocationAreaResponse
	err = json.Unmarshal(body, &locationAreasResp)
	if err != nil {
		return fmt.Errorf("failed to unmarshal JSON response: %w", err)
	}

	fmt.Println("Location Areas (Previous):")
	for _, area := range locationAreasResp.Results {
		fmt.Println(area.Name)
	}

	cfg.NextLocationAreaURL = locationAreasResp.Next
	cfg.PrevLocationAreaURL = locationAreasResp.Previous

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

		command, exists := availableCommands[commandName]
		if exists {
			err := command.callback(cfg)

			if err != nil {
				fmt.Fprintln(os.Stderr, "Error executing command:", err)
			}
		} else {
			fmt.Println("Unknown command. Type 'help' for available commands.")
		}
	}
}

func main() {
	// Initialize the config
	initialNextURL := "https://pokeapi.co/api/v2/location-area/"

	cfg := Config{
		PokeapiClient: http.Client{
			Timeout: 10 * time.Second,
		},
		NextLocationAreaURL: &initialNextURL,
		PrevLocationAreaURL: nil,
	}
	startRepl(&cfg)
}
