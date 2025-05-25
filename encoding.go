package main

import (
	"crypto/rand"
	"crypto/sha256"
	"errors"
	"math"
	"math/big"
)

func CreateSuperposition(states []complex128) Superposition {
	sum := 0.0
	amplitudes := make([]float64, len(states))

	for i := range states {
		r, _ := rand.Int(rand.Reader, big.NewInt(100))
		val := float64(r.Int64()) + 1
		sum += val
		amplitudes[i] = val
	}

	// Normalize amplitudes
	for i := range amplitudes {
		amplitudes[i] /= sum
	}

	return Superposition{
		States:     states,
		Amplitudes: amplitudes,
	}
}

func (s Superposition) CoordinatesAsSlices() [][]float64 {
	out := make([][]float64, len(s.States))
	for i, c := range s.States {
		out[i] = []float64{real(c), imag(c)}
	}
	return out
}

// BytesToState converts arbitrary bytes to a normalized quantum state vector.
// The function uses SHA-256 to deterministically generate a state vector from the input bytes.
// The resulting state vector will have a length that is a power of 2 (for quantum compatibility).
func BytesToState(data []byte, targetSize int) ([]complex128, error) {
	if len(data) == 0 {
		return nil, errors.New("input data cannot be empty")
	}

	// Ensure target size is a power of 2 and reasonable
	if targetSize <= 0 || (targetSize&(targetSize-1)) != 0 {
		return nil, errors.New("target size must be a positive power of 2")
	}

	// Use SHA-256 to create deterministic pseudo-random values from the input bytes
	hasher := sha256.New()
	hasher.Write(data)
	seed := hasher.Sum(nil)

	// Generate complex numbers from the hash
	states := make([]complex128, targetSize)

	// Use the hash bytes to seed deterministic generation
	// We'll use multiple rounds of hashing to get enough entropy
	for i := 0; i < targetSize; i++ {
		// Create a new hash for each complex number to ensure good distribution
		roundHasher := sha256.New()
		roundHasher.Write(seed)
		roundHasher.Write([]byte{byte(i), byte(i >> 8), byte(i >> 16), byte(i >> 24)})
		roundHash := roundHasher.Sum(nil)

		// Use first 8 bytes for real part, next 8 for imaginary part
		realBytes := roundHash[0:8]
		imagBytes := roundHash[8:16]

		// Convert bytes to float64 values in range [-1, 1]
		realVal := bytesToFloat(realBytes)
		imagVal := bytesToFloat(imagBytes)

		states[i] = complex(realVal, imagVal)
	}

	// Normalize the state vector to ensure it's a valid quantum state
	return normalizeStateVector(states), nil
}

// bytesToFloat converts 8 bytes to a float64 in range [-1, 1]
func bytesToFloat(bytes []byte) float64 {
	if len(bytes) < 8 {
		return 0.0
	}

	// Convert bytes to uint64
	var val uint64
	for i := 0; i < 8; i++ {
		val = (val << 8) | uint64(bytes[i])
	}

	// Convert to float in range [0, 1]
	normalized := float64(val) / float64(^uint64(0))

	// Convert to range [-1, 1]
	return 2.0*normalized - 1.0
}

// normalizeStateVector normalizes a quantum state vector so that sum(|c|^2) = 1
func normalizeStateVector(states []complex128) []complex128 {
	// Calculate the norm
	var norm float64
	for _, c := range states {
		r := real(c)
		i := imag(c)
		norm += r*r + i*i
	}

	if norm == 0 {
		// Handle zero vector case - create a simple normalized state
		states[0] = complex(1.0, 0.0)
		return states
	}

	// Normalize
	normSqrt := math.Sqrt(norm)
	normalized := make([]complex128, len(states))
	for i, c := range states {
		normalized[i] = c / complex(normSqrt, 0)
	}

	return normalized
}

// CreateDeterministicSuperposition creates a superposition with deterministic amplitudes
// based on the state vector itself, rather than random values.
func CreateDeterministicSuperposition(states []complex128) Superposition {
	amplitudes := make([]float64, len(states))

	// Use the magnitude of each state as the amplitude (deterministic)
	var sum float64
	for i, state := range states {
		magnitude := real(state)*real(state) + imag(state)*imag(state)
		amplitudes[i] = magnitude
		sum += magnitude
	}

	// Normalize amplitudes
	if sum > 0 {
		for i := range amplitudes {
			amplitudes[i] /= sum
		}
	} else {
		// Handle edge case where all states are zero
		for i := range amplitudes {
			amplitudes[i] = 1.0 / float64(len(amplitudes))
		}
	}

	return Superposition{
		States:     states,
		Amplitudes: amplitudes,
	}
}

// calculateEntanglement calculates the entanglement measure for a quantum state
func calculateEntanglement(states []complex128) float64 {
	if len(states) <= 1 {
		return 0.0
	}

	// Calculate von Neumann entropy as a measure of entanglement
	var entropy float64
	for _, state := range states {
		prob := real(state)*real(state) + imag(state)*imag(state)
		if prob > 1e-10 { // Avoid log(0)
			entropy -= prob * math.Log2(prob)
		}
	}

	// Normalize by maximum possible entropy for this dimension
	maxEntropy := math.Log2(float64(len(states)))
	if maxEntropy > 0 {
		return entropy / maxEntropy
	}
	return 0.0
}

// calculateCoherence calculates the coherence measure for a quantum state
func calculateCoherence(states []complex128) float64 {
	if len(states) == 0 {
		return 0.0
	}

	// Calculate l1-norm of coherence (sum of off-diagonal elements)
	var coherence float64
	for i, state := range states {
		magnitude := math.Sqrt(real(state)*real(state) + imag(state)*imag(state))
		coherence += magnitude

		// Add phase contribution for superposition states
		if i > 0 && magnitude > 1e-10 {
			phase := math.Atan2(imag(state), real(state))
			coherence += math.Abs(math.Sin(phase))
		}
	}

	return coherence
}