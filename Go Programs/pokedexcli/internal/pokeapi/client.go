package pokeapi

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"

	"github.com/Exonymos/pokedexcli/internal/pokecache"
)

const (
	BaseURL = "https://pokeapi.co/api/v2"
)

// Client is a client for interacting with the PokeAPI.
type Client struct {
	httpClient http.Client
	cache      *pokecache.Cache
}

// NewClient creates a new PokeAPI client.
func NewClient(cache *pokecache.Cache, timeout time.Duration) Client {
	return Client{
		httpClient: http.Client{
			Timeout: timeout,
		},
		cache: cache,
	}
}

// ListLocationAreas fetches a list of location areas.
func (c *Client) ListLocationAreas(pageURL *string) (LocationAreaResponse, error) {
	url := BaseURL + "/location-area/"
	if pageURL != nil && *pageURL != "" {
		url = *pageURL
	}

	var data LocationAreaResponse
	body, err := c.makeRequest(url)
	if err != nil {
		return LocationAreaResponse{}, err
	}

	err = json.Unmarshal(body, &data)
	if err != nil {
		return LocationAreaResponse{}, fmt.Errorf("failed to unmarshal location areas response: %w (Body: %s)", err, string(body))
	}
	return data, nil
}

// GetLocationAreaDetail fetches details for a specific location area.
func (c *Client) GetLocationAreaDetail(areaName string) (LocationAreaDetailResponse, error) {
	url := fmt.Sprintf("%s/location-area/%s/", BaseURL, areaName)

	var data LocationAreaDetailResponse
	body, err := c.makeRequest(url)
	if err != nil {
		return LocationAreaDetailResponse{}, err
	}

	err = json.Unmarshal(body, &data)
	if err != nil {
		return LocationAreaDetailResponse{}, fmt.Errorf("failed to unmarshal location area detail response for %s: %w (Body: %s)", areaName, err, string(body))
	}
	return data, nil
}

// GetPokemonInfo fetches information about a specific Pokemon.
func (c *Client) GetPokemonInfo(pokemonName string) (PokemonApiResponse, error) {
	url := fmt.Sprintf("%s/pokemon/%s/", BaseURL, pokemonName)

	var data PokemonApiResponse
	body, err := c.makeRequest(url)
	if err != nil {
		return PokemonApiResponse{}, err
	}

	err = json.Unmarshal(body, &data)
	if err != nil {
		return PokemonApiResponse{}, fmt.Errorf("failed to unmarshal pokemon info response for %s: %w (Body: %s)", pokemonName, err, string(body))
	}
	return data, nil
}

// makeRequest is a helper to handle caching and HTTP GET requests.
func (c *Client) makeRequest(url string) ([]byte, error) {
	// Try to get from cache first
	if c.cache != nil {
		cachedData, found := c.cache.Get(url)
		if found {
			fmt.Printf("(API Client: Cache hit for %s)\n", url)
			return cachedData, nil
		}
		fmt.Printf("(API Client: Cache miss for %s, fetching...)\n", url)
	} else {
		fmt.Printf("(API Client: No cache provided, fetching %s...)\n", url)
	}

	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return nil, fmt.Errorf("failed to create request for %s: %w", url, err)
	}

	resp, err := c.httpClient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("failed to execute request for %s: %w", url, err)
	}
	defer resp.Body.Close()

	if resp.StatusCode == http.StatusNotFound {
		// Return a specific error or indicator for 404
		return nil, fmt.Errorf("resource not found (404) at %s", url)
	}
	if resp.StatusCode > 299 {
		bodyBytes, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("bad status code: %d from %s. Response: %s", resp.StatusCode, url, string(bodyBytes))
	}

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("failed to read response body from %s: %w", url, err)
	}

	// Add to cache if cache is available
	if c.cache != nil {
		c.cache.Add(url, body)
	}
	return body, nil
}
