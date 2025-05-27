package main

import (
	"encoding/hex"
	"lukechampine.com/blake3"
)

// CreateEntangledState produces an entangled hash state from encoded states using keyed hashing
func CreateEntangledState(states []string, key []byte, size int) string {
	hasher := blake3.New(size, key)
	for _, state := range states {
		hasher.Write([]byte(state))
	}
	return hex.EncodeToString(hasher.Sum(nil))
}
