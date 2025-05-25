package main

import (
	"sync"
)

type ResultCache struct {
	cache map[string]interface{}
	mu    sync.RWMutex
}

func NewResultCache() *ResultCache {
	return &ResultCache{
		cache: make(map[string]interface{}),
	}
}

func (rc *ResultCache) Get(key string) (interface{}, bool) {
	rc.mu.RLock()
	defer rc.mu.RUnlock()
	val, ok := rc.cache[key]
	return val, ok
}

func (rc *ResultCache) Set(key string, val interface{}) {
	rc.mu.Lock()
	defer rc.mu.Unlock()
	rc.cache[key] = val
}
