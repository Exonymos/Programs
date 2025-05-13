package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strings"
)

// cliCommand struct definition
type cliCommand struct {
	name        string
	description string
	callback    func() error
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
	}
}

// callback for the "exit" command
func commandExit() error {
	fmt.Println("Closing the Pokedex... Goodbye!")
	os.Exit(0)
	return nil
}

// callback for the "help" command
func commandHelp() error {
	fmt.Println("\nWelcome to the Pokedex!")
	fmt.Println("Usage:")
	fmt.Println("")

	// Access commands dynamically
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

func cleanInput(text string) []string {
	output := strings.ToLower(text)
	output = strings.TrimSpace(output)
	words := strings.Fields(output)
	if len(words) == 0 {
		return []string{}
	}
	return words
}

func startRepl() {
	scanner := bufio.NewScanner(os.Stdin)
	availableCommands := getCommands()

	// Get command names and sort them for consistent help output
	var commandNames []string
	for name := range availableCommands {
		commandNames = append(commandNames, name)
	}
	sort.Strings(commandNames)

	for _, name := range commandNames {
		cmd := availableCommands[name]
		fmt.Printf("%s: %s\n", cmd.name, cmd.description)
	}

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
			err := command.callback()

			if err != nil {
				fmt.Fprintln(os.Stderr, "Error executing command:", err)
			}
		} else {
			fmt.Println("Unknown command. Type 'help' for available commands.")
		}
	}
}

func main() {
	startRepl()
}
