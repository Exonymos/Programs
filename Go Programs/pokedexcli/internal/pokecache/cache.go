package pokecache

import (
	"sync"
	"time"
)

// cacheEntry stores the cached data and its creation time
type cacheEntry struct {
	createdAt time.Time
	val       []byte
}

// Cache is a thread-safe in-memory cache
type Cache struct {
	mu           sync.Mutex
	entries      map[string]cacheEntry
	reapInterval time.Duration
}

// NewCache creates a new Cache instance with a given reap interval
// The reapLoop will remove entries older than this interval
func NewCache(reapInterval time.Duration) *Cache {
	c := &Cache{
		entries:      make(map[string]cacheEntry),
		reapInterval: reapInterval,
	}
	go c.reapLoop()
	return c
}

// Add adds a new entry to the cache
func (c *Cache) Add(key string, val []byte) {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.entries[key] = cacheEntry{
		createdAt: time.Now().UTC(),
		val:       val,
	}
}

// Get retrieves an entry from the cache
// It returns the value and true if found, otherwise nil and false
func (c *Cache) Get(key string) ([]byte, bool) {
	c.mu.Lock()
	defer c.mu.Unlock()
	entry, ok := c.entries[key]
	if !ok {
		return nil, false
	}
	return entry.val, true
}

// reapLoop periodically removes stale entries from the cache
func (c *Cache) reapLoop() {
	ticker := time.NewTicker(c.reapInterval)
	defer ticker.Stop()

	for range ticker.C {
		c.mu.Lock()
		// Iterate over all cache entries
		for key, entry := range c.entries {
			// If an entry is older than the reapInterval, remove it
			if time.Since(entry.createdAt) > c.reapInterval {
				delete(c.entries, key)
			}
		}
		c.mu.Unlock()
	}
}
