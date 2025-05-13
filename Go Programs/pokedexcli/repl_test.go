package main

import (
	"reflect" // Used for DeepEqual
	"testing"
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
