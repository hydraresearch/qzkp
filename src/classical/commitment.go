package main

import (
	"fmt"
	"lukechampine.com/blake3"
)

func GenerateCommitment(superpos Superposition, identifier string, key []byte) []byte {
	// Ensure key is exactly 32 bytes for blake3
	var blake3Key [32]byte
	if len(key) >= 32 {
		copy(blake3Key[:], key[:32])
	} else {
		copy(blake3Key[:], key)
		// Pad with zeros if key is shorter
	}

	hasher := blake3.New(32, blake3Key[:])

	// Include both states and amplitudes
	for i, coord := range superpos.States {
		hasher.Write([]byte(fmt.Sprintf("%f%f", real(coord), imag(coord))))
		hasher.Write([]byte(fmt.Sprintf("%f", superpos.Amplitudes[i])))
	}

	hasher.Write([]byte(identifier))
	return hasher.Sum(nil)
}
