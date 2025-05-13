package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

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

	for {
		fmt.Print("Pokedex > ")

		// Wait for user input
		scanned := scanner.Scan()
		if !scanned {
			// Handle EOF or scanner error
			if err := scanner.Err(); err != nil {
				fmt.Println("Error reading input:", err)
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

		fmt.Printf("Your command was: %s\n", commandName)
	}
}

func main() {
	startRepl()
}
