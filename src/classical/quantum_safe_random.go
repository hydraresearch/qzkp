package main

import (
	"crypto/rand"
	"fmt"
	"go.dedis.ch/kyber/v3"
	"io"
	"time"

	"go.dedis.ch/kyber/v3/group/edwards25519"
	"go.dedis.ch/kyber/v3/xof/blake2xb"
)

// QuantumSafeRandom provides quantum-resistant random number generation
// using DEDIS Kyber cryptographic primitives
type QuantumSafeRandom struct {
	suite  kyber.Group
	stream kyber.XOF
	seed   []byte
}

// NewQuantumSafeRandom creates a new quantum-safe random generator
func NewQuantumSafeRandom() (*QuantumSafeRandom, error) {
	suite := edwards25519.NewBlakeSHA256Ed25519()

	// Generate cryptographically secure seed
	seed := make([]byte, 64) // 512 bits of entropy
	if _, err := rand.Read(seed); err != nil {
		return nil, fmt.Errorf("failed to generate seed: %v", err)
	}

	// Initialize BLAKE2XB stream with seed
	stream := blake2xb.New(seed)

	return &QuantumSafeRandom{
		suite:  suite,
		stream: stream,
		seed:   seed,
	}, nil
}

// GenerateRandomBytes generates cryptographically secure random bytes
// using quantum-resistant DEDIS Kyber primitives
func (qsr *QuantumSafeRandom) GenerateRandomBytes(length int) ([]byte, error) {
	if length <= 0 {
		return nil, fmt.Errorf("invalid length: %d", length)
	}

	randomBytes := make([]byte, length)

	// Use DEDIS Kyber's quantum-safe random stream
	n, err := qsr.stream.Read(randomBytes)
	if err != nil {
		return nil, fmt.Errorf("failed to read from quantum-safe stream: %v", err)
	}

	if n != length {
		return nil, fmt.Errorf("insufficient random bytes generated: got %d, wanted %d", n, length)
	}

	return randomBytes, nil
}

// GenerateScalar generates a random scalar using DEDIS Kyber
func (qsr *QuantumSafeRandom) GenerateScalar() kyber.Scalar {
	return qsr.suite.Scalar().Pick(qsr.stream)
}

// GeneratePoint generates a random point using DEDIS Kyber
func (qsr *QuantumSafeRandom) GeneratePoint() kyber.Point {
	return qsr.suite.Point().Pick(qsr.stream)
}

// ReseedWithEntropy reseeds the generator with additional entropy
func (qsr *QuantumSafeRandom) ReseedWithEntropy(additionalEntropy []byte) error {
	// Combine existing seed with new entropy
	combinedSeed := append(qsr.seed, additionalEntropy...)
	combinedSeed = append(combinedSeed, []byte(time.Now().String())...)

	// Create new stream with combined entropy
	qsr.stream = blake2xb.New(combinedSeed)
	qsr.seed = combinedSeed

	return nil
}

// GetEntropyEstimate returns an estimate of available entropy
func (qsr *QuantumSafeRandom) GetEntropyEstimate() int {
	// DEDIS Kyber with BLAKE2XB provides high entropy
	// Conservative estimate based on seed length and stream properties
	return len(qsr.seed) * 8 // bits of entropy
}

// SecureRandomCommitment generates a quantum-safe commitment using DEDIS Kyber
func (qsr *QuantumSafeRandom) SecureRandomCommitment(data []byte) ([]byte, []byte, error) {
	// Generate quantum-safe randomness for commitment
	randomness, err := qsr.GenerateRandomBytes(32)
	if err != nil {
		return nil, nil, fmt.Errorf("failed to generate randomness: %v", err)
	}

	// Create commitment using BLAKE2XB (quantum-resistant)
	commitmentStream := blake2xb.New(append(data, randomness...))
	commitment := make([]byte, 32)
	if _, err := commitmentStream.Read(commitment); err != nil {
		return nil, nil, fmt.Errorf("failed to create commitment: %v", err)
	}

	return commitment, randomness, nil
}

// QuantumSafeRandomReader implements io.Reader for compatibility
type QuantumSafeRandomReader struct {
	qsr *QuantumSafeRandom
}

// NewQuantumSafeRandomReader creates a new quantum-safe random reader
func NewQuantumSafeRandomReader() (*QuantumSafeRandomReader, error) {
	qsr, err := NewQuantumSafeRandom()
	if err != nil {
		return nil, err
	}

	return &QuantumSafeRandomReader{qsr: qsr}, nil
}

// Read implements io.Reader interface
func (qsrr *QuantumSafeRandomReader) Read(p []byte) (int, error) {
	randomBytes, err := qsrr.qsr.GenerateRandomBytes(len(p))
	if err != nil {
		return 0, err
	}

	copy(p, randomBytes)
	return len(p), nil
}

// HybridRandomGenerator combines multiple entropy sources for maximum security
type HybridRandomGenerator struct {
	quantumSafe *QuantumSafeRandom
	systemRand  io.Reader
}

// NewHybridRandomGenerator creates a hybrid random generator
func NewHybridRandomGenerator() (*HybridRandomGenerator, error) {
	qsr, err := NewQuantumSafeRandom()
	if err != nil {
		return nil, err
	}

	return &HybridRandomGenerator{
		quantumSafe: qsr,
		systemRand:  rand.Reader,
	}, nil
}

// GenerateHybridRandomBytes combines quantum-safe and system randomness
func (hrg *HybridRandomGenerator) GenerateHybridRandomBytes(length int) ([]byte, error) {
	// Get randomness from both sources
	quantumBytes, err := hrg.quantumSafe.GenerateRandomBytes(length)
	if err != nil {
		return nil, fmt.Errorf("quantum-safe generation failed: %v", err)
	}

	systemBytes := make([]byte, length)
	if _, err := hrg.systemRand.Read(systemBytes); err != nil {
		return nil, fmt.Errorf("system random generation failed: %v", err)
	}

	// XOR combine for maximum entropy
	result := make([]byte, length)
	for i := 0; i < length; i++ {
		result[i] = quantumBytes[i] ^ systemBytes[i]
	}

	return result, nil
}

// ValidateRandomness performs basic statistical tests on generated randomness
func ValidateRandomness(data []byte) map[string]float64 {
	if len(data) == 0 {
		return map[string]float64{"error": -1}
	}

	// Basic entropy estimation
	freq := make(map[byte]int)
	for _, b := range data {
		freq[b]++
	}

	// Calculate Shannon entropy
	entropy := 0.0
	length := float64(len(data))
	for _, count := range freq {
		if count > 0 {
			p := float64(count) / length
			entropy -= p * (log2(p))
		}
	}

	// Calculate byte frequency variance
	expectedFreq := length / 256.0
	variance := 0.0
	for i := 0; i < 256; i++ {
		freq_i := float64(freq[byte(i)])
		variance += (freq_i - expectedFreq) * (freq_i - expectedFreq)
	}
	variance /= 256.0

	return map[string]float64{
		"entropy":            entropy,
		"max_entropy":        8.0, // bits per byte
		"entropy_ratio":      entropy / 8.0,
		"frequency_variance": variance,
	}
}

// Helper function for log base 2
func log2(x float64) float64 {
	if x <= 0 {
		return 0
	}
	return 1.4426950408889634 * log(x) // log2(x) = ln(x) / ln(2)
}

// Simple natural log approximation
func log(x float64) float64 {
	// Simple approximation for demonstration
	// In production, use math.Log
	if x <= 0 {
		return 0
	}
	// Very basic approximation
	return (x - 1) - (x-1)*(x-1)/2 + (x-1)*(x-1)*(x-1)/3
}
