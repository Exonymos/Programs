package main

import (
	"bytes"
	"errors"
	"fmt"
	"io"
	"math/rand"
	"os"
	"reflect"
	"strings"
	"testing"
	"time"

	"github.com/Exonymos/pokedexcli/internal/pokeapi"
)

func TestCleanInput(t *testing.T) {
	cases := []struct {
		input    string
		expected []string
	}{
		{
			input:    "  hello  world  ",
			expected: []string{"hello", "world"},
		},
		{
			input:    "Charmander Bulbasaur PIKACHU",
			expected: []string{"charmander", "bulbasaur", "pikachu"},
		},
		{
			input:    "   ",
			expected: []string{},
		},
		{
			input:    "single",
			expected: []string{"single"},
		},
		{
			input:    "  LeadingAndTrailing  ",
			expected: []string{"leadingandtrailing"},
		},
	}

	for _, c := range cases {
		actual := cleanInput(c.input)
		if len(actual) != len(c.expected) {
			if len(c.expected) == 0 && len(actual) == 0 {

			} else {
				t.Errorf("Lengths don't match for input '%s': expected %d, got %d (actual: %v, expected: %v)",
					c.input, len(c.expected), len(actual), actual, c.expected)
				continue
			}
		}

		if !reflect.DeepEqual(actual, c.expected) {
			t.Errorf("cleanInput(%q) == %v, want %v", c.input, actual, c.expected)
		}
	}
}

// Mock API Client for command testing

// MockPokeAPIClient is a mock implementation of the pokeapi.APIClient
type MockPokeAPIClient struct {
	MockListLocationAreas     func(pageURL *string) (pokeapi.LocationAreaResponse, error)
	MockGetLocationAreaDetail func(areaName string) (pokeapi.LocationAreaDetailResponse, error)
	MockGetPokemonInfo        func(pokemonName string) (pokeapi.PokemonApiResponse, error)
}

// Implement the APIClient interface
func (m *MockPokeAPIClient) ListLocationAreas(pageURL *string) (pokeapi.LocationAreaResponse, error) {
	if m.MockListLocationAreas != nil {
		return m.MockListLocationAreas(pageURL)
	}
	return pokeapi.LocationAreaResponse{}, errors.New("MockListLocationAreas not implemented in mock")
}

func (m *MockPokeAPIClient) GetLocationAreaDetail(areaName string) (pokeapi.LocationAreaDetailResponse, error) {
	if m.MockGetLocationAreaDetail != nil {
		return m.MockGetLocationAreaDetail(areaName)
	}
	return pokeapi.LocationAreaDetailResponse{}, errors.New("MockGetLocationAreaDetail not implemented in mock")
}

func (m *MockPokeAPIClient) GetPokemonInfo(pokemonName string) (pokeapi.PokemonApiResponse, error) {
	if m.MockGetPokemonInfo != nil {
		return m.MockGetPokemonInfo(pokemonName)
	}
	return pokeapi.PokemonApiResponse{}, errors.New("MockGetPokemonInfo not implemented in mock")
}

// Command Logic Tests

func TestCommandMap(t *testing.T) {
	// Test case 1: Successful fetch of initial page
	t.Run("successful initial fetch", func(t *testing.T) {
		initialNextURL := pokeapi.BaseURL + "/location-area/"
		cfg := &Config{
			UserPokedex:         make(map[string]pokeapi.PokemonApiResponse),
			NextLocationAreaURL: &initialNextURL,
		}
		mockClient := &MockPokeAPIClient{}
		cfg.PokeAPIClient = mockClient

		expectedNextURL := "http://example.com/next"
		var expectedPrevURL *string = nil
		expectedResults := []struct {
			Name string `json:"name"`
			URL  string `json:"url"`
		}{
			{Name: "area1", URL: "url1"},
			{Name: "area2", URL: "url2"},
		}

		mockClient.MockListLocationAreas = func(pageURL *string) (pokeapi.LocationAreaResponse, error) {
			if pageURL == nil || *pageURL != initialNextURL {
				t.Errorf("commandMap called ListLocationAreas with unexpected URL: got %v, want %s", pageURL, initialNextURL)
			}
			return pokeapi.LocationAreaResponse{
				Next:     &expectedNextURL,
				Previous: expectedPrevURL,
				Results:  expectedResults,
			}, nil
		}

		oldStdout := os.Stdout
		r, w, _ := os.Pipe()
		os.Stdout = w

		err := commandMap(cfg)

		w.Close()
		os.Stdout = oldStdout
		var buf bytes.Buffer
		io.Copy(&buf, r)
		output := buf.String()

		if err != nil {
			t.Fatalf("commandMap failed: %v", err)
		}

		if cfg.NextLocationAreaURL == nil || *cfg.NextLocationAreaURL != expectedNextURL {
			t.Errorf("expected NextLocationAreaURL to be '%s', got '%v'", expectedNextURL, cfg.NextLocationAreaURL)
		}
		if cfg.PrevLocationAreaURL != expectedPrevURL {
			if !(cfg.PrevLocationAreaURL == nil && expectedPrevURL == nil) {
				if cfg.PrevLocationAreaURL == nil || expectedPrevURL == nil || *cfg.PrevLocationAreaURL != *expectedPrevURL {
					t.Errorf("expected PrevLocationAreaURL to be '%v', got '%v'", expectedPrevURL, cfg.PrevLocationAreaURL)
				}
			}
		}

		if !strings.Contains(output, "Location Areas:") {
			t.Errorf("output does not contain 'Location Areas:':\n%s", output)
		}
		if !strings.Contains(output, "area1") {
			t.Errorf("output does not contain 'area1':\n%s", output)
		}
		if !strings.Contains(output, "area2") {
			t.Errorf("output does not contain 'area2':\n%s", output)
		}
	})

	// Test case 2: API error
	t.Run("api error", func(t *testing.T) {
		initialNextURL := pokeapi.BaseURL + "/location-area/"
		cfg := &Config{
			UserPokedex:         make(map[string]pokeapi.PokemonApiResponse),
			NextLocationAreaURL: &initialNextURL,
		}
		mockClient := &MockPokeAPIClient{}
		cfg.PokeAPIClient = mockClient

		expectedErrorMsg := "simulated API error"
		mockClient.MockListLocationAreas = func(pageURL *string) (pokeapi.LocationAreaResponse, error) {
			return pokeapi.LocationAreaResponse{}, errors.New(expectedErrorMsg)
		}

		err := commandMap(cfg)
		if err == nil {
			t.Fatalf("commandMap expected an error, but got nil")
		}
		if !strings.Contains(err.Error(), expectedErrorMsg) {
			t.Errorf("commandMap error message '%s' does not contain expected '%s'", err.Error(), expectedErrorMsg)
		}
	})

	// Test case 3: Fetching with an existing NextLocationAreaURL from config
	t.Run("successful fetch with next page URL from config", func(t *testing.T) {
		currentNextURL := "http://initial.com/nextpage"
		cfg := &Config{
			NextLocationAreaURL: &currentNextURL,
			UserPokedex:         make(map[string]pokeapi.PokemonApiResponse),
		}
		mockClient := &MockPokeAPIClient{}
		cfg.PokeAPIClient = mockClient

		expectedUpdatedNextURL := "http://example.com/next2"
		expectedResults := []struct {
			Name string `json:"name"`
			URL  string `json:"url"`
		}{
			{Name: "area3", URL: "url3"},
		}

		mockClient.MockListLocationAreas = func(pageURL *string) (pokeapi.LocationAreaResponse, error) {
			if pageURL == nil || *pageURL != currentNextURL {
				t.Errorf("Expected ListLocationAreas to be called with URL '%s', got '%v'", currentNextURL, pageURL)
			}
			return pokeapi.LocationAreaResponse{
				Next:    &expectedUpdatedNextURL,
				Results: expectedResults,
			}, nil
		}

		oldStdout := os.Stdout
		r, w, _ := os.Pipe()
		os.Stdout = w

		err := commandMap(cfg)

		w.Close()
		os.Stdout = oldStdout
		var buf bytes.Buffer
		io.Copy(&buf, r)
		output := buf.String()

		if err != nil {
			t.Fatalf("commandMap failed: %v", err)
		}
		if cfg.NextLocationAreaURL == nil || *cfg.NextLocationAreaURL != expectedUpdatedNextURL {
			t.Errorf("expected NextLocationAreaURL to be updated to '%s', got '%v'", expectedUpdatedNextURL, cfg.NextLocationAreaURL)
		}
		if !strings.Contains(output, "area3") {
			t.Errorf("output does not contain 'area3':\n%s", output)
		}
	})
}

func TestCommandPokedex(t *testing.T) {
	// Helper function to capture stdout for pokedex command tests
	capturePokedexOutput := func(cfg *Config) (string, error) {
		oldStdout := os.Stdout
		r, w, _ := os.Pipe()
		os.Stdout = w

		err := commandPokedex(cfg)

		w.Close()
		os.Stdout = oldStdout
		var buf bytes.Buffer
		io.Copy(&buf, r)
		return buf.String(), err
	}

	t.Run("empty pokedex", func(t *testing.T) {
		cfg := &Config{
			UserPokedex: make(map[string]pokeapi.PokemonApiResponse),
		}

		output, err := capturePokedexOutput(cfg)
		if err != nil {
			t.Fatalf("commandPokedex failed for empty pokedex: %v", err)
		}

		expectedOutput := "Your Pokedex is empty. Go catch some Pokemon!"
		if !strings.Contains(output, expectedOutput) {
			t.Errorf("expected output to contain '%s', got:\n%s", expectedOutput, output)
		}
	})

	t.Run("pokedex with entries", func(t *testing.T) {
		cfg := &Config{
			UserPokedex: map[string]pokeapi.PokemonApiResponse{
				"pikachu":    {Name: "pikachu"},
				"bulbasaur":  {Name: "bulbasaur"},
				"charmander": {Name: "charmander"},
			},
		}

		output, err := capturePokedexOutput(cfg)
		if err != nil {
			t.Fatalf("commandPokedex failed for non-empty pokedex: %v", err)
		}

		// Check for the header and all Pokemon names
		if !strings.Contains(output, "Your Pokedex:") {
			t.Errorf("output missing 'Your Pokedex:' heading, got:\n%s", output)
		}
		if !strings.Contains(output, " - bulbasaur") {
			t.Errorf("output missing ' - bulbasaur', got:\n%s", output)
		}
		if !strings.Contains(output, " - charmander") {
			t.Errorf("output missing ' - charmander', got:\n%s", output)
		}
		if !strings.Contains(output, " - pikachu") {
			t.Errorf("output missing ' - pikachu', got:\n%s", output)
		}
	})
}

func TestCommandMapb(t *testing.T) {
	t.Run("successful previous page fetch", func(t *testing.T) {
		// Initial state: assume we are on page 2, so PrevLocationAreaURL is set
		prevURLFromConfig := "http://api.example.com/page1"
		cfg := &Config{
			PrevLocationAreaURL: &prevURLFromConfig,
			UserPokedex:         make(map[string]pokeapi.PokemonApiResponse),
		}
		mockClient := &MockPokeAPIClient{}
		cfg.PokeAPIClient = mockClient

		// Expected response when fetching prevURLFromConfig (i.e., page 1)
		expectedNextURL := prevURLFromConfig // Next from page 1 would be page 2 (current prev)
		var expectedPrevURL *string = nil    // Previous from page 1 is nil
		expectedResults := []struct {
			Name string `json:"name"`
			URL  string `json:"url"`
		}{
			{Name: "prev_area1", URL: "prev_url1"},
		}

		mockClient.MockListLocationAreas = func(pageURL *string) (pokeapi.LocationAreaResponse, error) {
			if pageURL == nil || *pageURL != prevURLFromConfig {
				t.Errorf("commandMapb called ListLocationAreas with unexpected URL: got %v, want %s", pageURL, prevURLFromConfig)
			}
			return pokeapi.LocationAreaResponse{
				Next:     &expectedNextURL,
				Previous: expectedPrevURL,
				Results:  expectedResults,
			}, nil
		}

		oldStdout := os.Stdout
		r, w, _ := os.Pipe()
		os.Stdout = w
		err := commandMapb(cfg)
		w.Close()
		os.Stdout = oldStdout
		var buf bytes.Buffer
		io.Copy(&buf, r)
		output := buf.String()

		if err != nil {
			t.Fatalf("commandMapb failed: %v", err)
		}
		if cfg.NextLocationAreaURL == nil || *cfg.NextLocationAreaURL != expectedNextURL {
			t.Errorf("expected NextLocationAreaURL to be '%s', got '%v'", expectedNextURL, cfg.NextLocationAreaURL)
		}
		if cfg.PrevLocationAreaURL != expectedPrevURL {
			t.Errorf("expected PrevLocationAreaURL to be nil, got '%v'", cfg.PrevLocationAreaURL)
		}
		if !strings.Contains(output, "prev_area1") {
			t.Errorf("output does not contain 'prev_area1':\n%s", output)
		}
	})

	t.Run("already on first page", func(t *testing.T) {
		cfg := &Config{
			PrevLocationAreaURL: nil,
			UserPokedex:         make(map[string]pokeapi.PokemonApiResponse),
		}

		mockClient := &MockPokeAPIClient{}
		cfg.PokeAPIClient = mockClient
		mockClient.MockListLocationAreas = func(pageURL *string) (pokeapi.LocationAreaResponse, error) {
			t.Errorf("ListLocationAreas should not be called when on the first page for mapb")
			return pokeapi.LocationAreaResponse{}, errors.New("API should not be called")
		}

		oldStdout := os.Stdout
		r, w, _ := os.Pipe()
		os.Stdout = w
		err := commandMapb(cfg)
		w.Close()
		os.Stdout = oldStdout
		var buf bytes.Buffer
		io.Copy(&buf, r)
		output := buf.String()

		if err != nil {
			t.Fatalf("commandMapb failed when on first page: %v", err)
		}
		expectedMsg := "You're on the first page, cannot go back further."
		if !strings.Contains(output, expectedMsg) {
			t.Errorf("expected output '%s', got '%s'", expectedMsg, output)
		}
		if cfg.PrevLocationAreaURL != nil {
			t.Errorf("PrevLocationAreaURL should remain nil, got %v", cfg.PrevLocationAreaURL)
		}
	})

	t.Run("api error on previous page fetch", func(t *testing.T) {
		prevURLFromConfig := "http://api.example.com/page1"
		cfg := &Config{
			PrevLocationAreaURL: &prevURLFromConfig,
			UserPokedex:         make(map[string]pokeapi.PokemonApiResponse),
		}
		mockClient := &MockPokeAPIClient{}
		cfg.PokeAPIClient = mockClient

		expectedErrorMsg := "simulated API error for mapb"
		mockClient.MockListLocationAreas = func(pageURL *string) (pokeapi.LocationAreaResponse, error) {
			return pokeapi.LocationAreaResponse{}, errors.New(expectedErrorMsg)
		}

		err := commandMapb(cfg)
		if err == nil {
			t.Fatalf("commandMapb expected an error, but got nil")
		}
		if !strings.Contains(err.Error(), expectedErrorMsg) {
			t.Errorf("commandMapb error message '%s' does not contain expected '%s'", err.Error(), expectedErrorMsg)
		}
	})
}

func TestCommandExplore(t *testing.T) {
	areaToExplore := "test-area"

	t.Run("successful exploration", func(t *testing.T) {
		cfg := &Config{UserPokedex: make(map[string]pokeapi.PokemonApiResponse)}
		mockClient := &MockPokeAPIClient{}
		cfg.PokeAPIClient = mockClient

		expectedEncounters := []struct {
			Pokemon struct {
				Name string `json:"name"`
				URL  string `json:"url"`
			} `json:"pokemon"`
		}{
			{Pokemon: struct {
				Name string `json:"name"`
				URL  string `json:"url"`
			}{Name: "pika", URL: "url_pika"}},
			{Pokemon: struct {
				Name string `json:"name"`
				URL  string `json:"url"`
			}{Name: "char", URL: "url_char"}},
		}

		mockClient.MockGetLocationAreaDetail = func(areaName string) (pokeapi.LocationAreaDetailResponse, error) {
			if areaName != areaToExplore {
				t.Errorf("GetLocationAreaDetail called with wrong area: got %s, want %s", areaName, areaToExplore)
			}
			return pokeapi.LocationAreaDetailResponse{
				Name:              areaName,
				PokemonEncounters: expectedEncounters,
			}, nil
		}

		oldStdout := os.Stdout
		r, w, _ := os.Pipe()
		os.Stdout = w
		err := commandExplore(cfg, areaToExplore)
		w.Close()
		os.Stdout = oldStdout
		var buf bytes.Buffer
		io.Copy(&buf, r)
		output := buf.String()

		if err != nil {
			t.Fatalf("commandExplore failed: %v", err)
		}
		if !strings.Contains(output, "Found Pokemon:") {
			t.Errorf("output missing 'Found Pokemon:' heading, got:\n%s", output)
		}
		if !strings.Contains(output, " - pika") {
			t.Errorf("output missing ' - pika', got:\n%s", output)
		}
		if !strings.Contains(output, " - char") {
			t.Errorf("output missing ' - char', got:\n%s", output)
		}
	})

	t.Run("exploration with no pokemon found", func(t *testing.T) {
		cfg := &Config{UserPokedex: make(map[string]pokeapi.PokemonApiResponse)}
		mockClient := &MockPokeAPIClient{}
		cfg.PokeAPIClient = mockClient

		var emptyEncounters []struct {
			Pokemon struct {
				Name string `json:"name"`
				URL  string `json:"url"`
			} `json:"pokemon"`
		}

		mockClient.MockGetLocationAreaDetail = func(areaName string) (pokeapi.LocationAreaDetailResponse, error) {
			return pokeapi.LocationAreaDetailResponse{
				Name:              areaName,
				PokemonEncounters: emptyEncounters,
			}, nil
		}

		oldStdout := os.Stdout
		r, w, _ := os.Pipe()
		os.Stdout = w
		err := commandExplore(cfg, areaToExplore)
		w.Close()
		os.Stdout = oldStdout
		var buf bytes.Buffer
		io.Copy(&buf, r)
		output := buf.String()

		if err != nil {
			t.Fatalf("commandExplore failed: %v", err)
		}
		expectedMsg := fmt.Sprintf("No Pokemon found in %s.", areaToExplore)
		if !strings.Contains(output, expectedMsg) {
			t.Errorf("expected output '%s', got '%s'", expectedMsg, output)
		}
	})

	t.Run("exploration api error", func(t *testing.T) {
		cfg := &Config{UserPokedex: make(map[string]pokeapi.PokemonApiResponse)}
		mockClient := &MockPokeAPIClient{}
		cfg.PokeAPIClient = mockClient

		expectedErrorMsg := "simulated API error for explore"
		mockClient.MockGetLocationAreaDetail = func(areaName string) (pokeapi.LocationAreaDetailResponse, error) {
			return pokeapi.LocationAreaDetailResponse{}, errors.New(expectedErrorMsg)
		}

		err := commandExplore(cfg, areaToExplore)
		if err == nil {
			t.Fatalf("commandExplore expected an error, but got nil")
		}
		if !strings.Contains(err.Error(), expectedErrorMsg) {
			t.Errorf("commandExplore error message '%s' does not contain expected '%s'", err.Error(), expectedErrorMsg)
		}
	})

	t.Run("no area name provided", func(t *testing.T) {
		cfg := &Config{UserPokedex: make(map[string]pokeapi.PokemonApiResponse)}
		mockClient := &MockPokeAPIClient{}
		cfg.PokeAPIClient = mockClient

		err := commandExplore(cfg)
		if err == nil {
			t.Fatalf("commandExplore expected an error for missing argument, but got nil")
		}
		if !strings.Contains(err.Error(), "please specify a location area name") {
			t.Errorf("commandExplore error message for missing argument is incorrect: %v", err)
		}
	})
}

func TestCommandCatch(t *testing.T) {
	rand.Seed(time.Now().UnixNano())
	pokemonToCatch := "pikachu"

	// Mock Pokemon data that would be returned by the API
	mockPikachuData := pokeapi.PokemonApiResponse{
		Name:           pokemonToCatch,
		BaseExperience: 112,
		Height:         4,
		Weight:         60,
		Stats: []struct {
			BaseStat int `json:"base_stat"`
			Stat     struct {
				Name string `json:"name"`
				URL  string `json:"url"`
			} `json:"stat"`
		}{
			{BaseStat: 35, Stat: struct {
				Name string `json:"name"`
				URL  string `json:"url"`
			}{Name: "hp"}},
		},
		Types: []struct {
			Slot int `json:"slot"`
			Type struct {
				Name string `json:"name"`
				URL  string `json:"url"`
			} `json:"type"`
		}{
			{Slot: 1, Type: struct {
				Name string `json:"name"`
				URL  string `json:"url"`
			}{Name: "electric"}},
		},
	}

	t.Run("successful catch", func(t *testing.T) {
		rand.Seed(time.Now().UnixNano() + 1)
		cfg := &Config{UserPokedex: make(map[string]pokeapi.PokemonApiResponse)}
		mockClient := &MockPokeAPIClient{}
		cfg.PokeAPIClient = mockClient

		// Mock GetPokemonInfo to return successfully
		mockClient.MockGetPokemonInfo = func(pokemonName string) (pokeapi.PokemonApiResponse, error) {
			if pokemonName != pokemonToCatch {
				t.Errorf("GetPokemonInfo called with wrong pokemon: got %s, want %s", pokemonName, pokemonToCatch)
			}

			dataToReturn := mockPikachuData
			dataToReturn.BaseExperience = 10
			return dataToReturn, nil
		}

		oldStdout := os.Stdout
		r, w, _ := os.Pipe()
		os.Stdout = w
		err := commandCatch(cfg, pokemonToCatch)
		w.Close()
		os.Stdout = oldStdout
		var buf bytes.Buffer
		io.Copy(&buf, r)
		output := buf.String()

		if err != nil {
			t.Fatalf("commandCatch failed: %v", err)
		}

		if !strings.Contains(output, fmt.Sprintf("%s was caught!", pokemonToCatch)) {
			t.Errorf("output missing catch success message, got:\n%s", output)
		}
		if _, caught := cfg.UserPokedex[pokemonToCatch]; !caught {
			t.Errorf("pokemon %s was not added to pokedex", pokemonToCatch)
		}
	})

	t.Run("pokemon escapes", func(t *testing.T) {
		rand.Seed(time.Now().UnixNano() + 2)
		cfg := &Config{UserPokedex: make(map[string]pokeapi.PokemonApiResponse)}
		mockClient := &MockPokeAPIClient{}
		cfg.PokeAPIClient = mockClient

		mockClient.MockGetPokemonInfo = func(pokemonName string) (pokeapi.PokemonApiResponse, error) {
			// To guarantee an escape, return high BaseExperience
			dataToReturn := mockPikachuData
			dataToReturn.BaseExperience = 1000
			return dataToReturn, nil
		}

		oldStdout := os.Stdout
		r, w, _ := os.Pipe()
		os.Stdout = w
		err := commandCatch(cfg, pokemonToCatch)
		w.Close()
		os.Stdout = oldStdout
		var buf bytes.Buffer
		io.Copy(&buf, r)
		output := buf.String()

		if err != nil {
			t.Fatalf("commandCatch failed: %v", err)
		}
		if !strings.Contains(output, fmt.Sprintf("%s escaped!", pokemonToCatch)) {
			t.Errorf("output missing escape message, got:\n%s", output)
		}
		if _, caught := cfg.UserPokedex[pokemonToCatch]; caught {
			t.Errorf("pokemon %s was added to pokedex on escape", pokemonToCatch)
		}
	})

	t.Run("pokemon not found by API", func(t *testing.T) {
		cfg := &Config{UserPokedex: make(map[string]pokeapi.PokemonApiResponse)}
		mockClient := &MockPokeAPIClient{}
		cfg.PokeAPIClient = mockClient

		mockedNotFoundError := fmt.Errorf("%w at test_url", pokeapi.ErrResourceNotFound)
		mockClient.MockGetPokemonInfo = func(pokemonName string) (pokeapi.PokemonApiResponse, error) {
			return pokeapi.PokemonApiResponse{}, mockedNotFoundError
		}

		oldStdout := os.Stdout
		r, w, _ := os.Pipe()
		os.Stdout = w
		err := commandCatch(cfg, "nonexistentpokemon")
		w.Close()
		os.Stdout = oldStdout
		var buf bytes.Buffer
		io.Copy(&buf, r)
		output := buf.String()

		if err != nil {
			t.Fatalf("commandCatch returned an error for 'not found' scenario: %v. It should return nil.", err)
		}
		if !strings.Contains(output, "Pokemon 'nonexistentpokemon' not found by API.") {
			t.Errorf("output missing 'not found by API' message, got:\n%s", output)
		}
	})

	t.Run("general api error", func(t *testing.T) {
		cfg := &Config{UserPokedex: make(map[string]pokeapi.PokemonApiResponse)}
		mockClient := &MockPokeAPIClient{}
		cfg.PokeAPIClient = mockClient

		expectedErrorMsg := "simulated general API error for catch"
		mockClient.MockGetPokemonInfo = func(pokemonName string) (pokeapi.PokemonApiResponse, error) {
			return pokeapi.PokemonApiResponse{}, errors.New(expectedErrorMsg)
		}

		err := commandCatch(cfg, pokemonToCatch)
		if err == nil {
			t.Fatalf("commandCatch expected an error, but got nil")
		}
		if !strings.Contains(err.Error(), expectedErrorMsg) {
			t.Errorf("commandCatch error message '%s' does not contain expected '%s'", err.Error(), expectedErrorMsg)
		}
	})

	t.Run("no pokemon name provided", func(t *testing.T) {
		cfg := &Config{UserPokedex: make(map[string]pokeapi.PokemonApiResponse)}
		err := commandCatch(cfg)
		if err == nil {
			t.Fatalf("commandCatch expected an error for missing argument, but got nil")
		}
		if !strings.Contains(err.Error(), "please specify a Pokemon name") {
			t.Errorf("commandCatch error message for missing argument is incorrect: %v", err)
		}
	})
}

func TestCommandInspect(t *testing.T) {
	pokemonName := "pikachu"
	mockPikachuData := pokeapi.PokemonApiResponse{
		Name:   pokemonName,
		Height: 4,
		Weight: 60,
		Stats: []struct {
			BaseStat int `json:"base_stat"`
			Stat     struct {
				Name string `json:"name"`
				URL  string `json:"url"`
			} `json:"stat"`
		}{
			{BaseStat: 35, Stat: struct {
				Name string `json:"name"`
				URL  string `json:"url"`
			}{Name: "hp"}},
			{BaseStat: 55, Stat: struct {
				Name string `json:"name"`
				URL  string `json:"url"`
			}{Name: "attack"}},
		},
		Types: []struct {
			Slot int `json:"slot"`
			Type struct {
				Name string `json:"name"`
				URL  string `json:"url"`
			} `json:"type"`
		}{
			{Slot: 1, Type: struct {
				Name string `json:"name"`
				URL  string `json:"url"`
			}{Name: "electric"}},
		},
	}

	t.Run("pokemon caught and inspected", func(t *testing.T) {
		cfg := &Config{
			UserPokedex: map[string]pokeapi.PokemonApiResponse{
				pokemonName: mockPikachuData,
			},
		}

		oldStdout := os.Stdout
		r, w, _ := os.Pipe()
		os.Stdout = w
		err := commandInspect(cfg, pokemonName)
		w.Close()
		os.Stdout = oldStdout
		var buf bytes.Buffer
		io.Copy(&buf, r)
		output := buf.String()

		if err != nil {
			t.Fatalf("commandInspect failed: %v", err)
		}
		if !strings.Contains(output, "Name: pikachu") {
			t.Errorf("output missing Name, got:\n%s", output)
		}
		if !strings.Contains(output, "Height: 4") {
			t.Errorf("output missing Height, got:\n%s", output)
		}
		if !strings.Contains(output, "Weight: 60") {
			t.Errorf("output missing Weight, got:\n%s", output)
		}
		if !strings.Contains(output, "-hp: 35") {
			t.Errorf("output missing hp stat, got:\n%s", output)
		}
		if !strings.Contains(output, "-attack: 55") {
			t.Errorf("output missing attack stat, got:\n%s", output)
		}
		if !strings.Contains(output, "- electric") {
			t.Errorf("output missing type electric, got:\n%s", output)
		}
	})

	t.Run("pokemon not caught", func(t *testing.T) {
		cfg := &Config{
			UserPokedex: make(map[string]pokeapi.PokemonApiResponse),
		}
		pokemonToInspect := "charizard"

		oldStdout := os.Stdout
		r, w, _ := os.Pipe()
		os.Stdout = w
		err := commandInspect(cfg, pokemonToInspect)
		w.Close()
		os.Stdout = oldStdout
		var buf bytes.Buffer
		io.Copy(&buf, r)
		output := buf.String()

		if err != nil {
			t.Fatalf("commandInspect failed: %v", err)
		}
		expectedMsg := fmt.Sprintf("You have not caught '%s' yet.", pokemonToInspect)
		if !strings.Contains(output, expectedMsg) {
			t.Errorf("expected output '%s', got '%s'", expectedMsg, output)
		}
	})

	t.Run("no pokemon name provided", func(t *testing.T) {
		cfg := &Config{UserPokedex: make(map[string]pokeapi.PokemonApiResponse)}
		err := commandInspect(cfg)
		if err == nil {
			t.Fatalf("commandInspect expected an error for missing argument, but got nil")
		}
		if !strings.Contains(err.Error(), "please specify a Pokemon name") {
			t.Errorf("commandInspect error message for missing argument is incorrect: %v", err)
		}
	})
}
