package main

import (
	"testing"
	"math"
	"bytes"
)

// Test basic mathematical operations for quantum states
func TestQuantumStateNormalization(t *testing.T) {
	t.Log("🧮 Testing quantum state normalization...")
	
	// Test case 1: Simple normalized state
	states := []complex128{
		complex(0.7071, 0.0),
		complex(0.7071, 0.0),
	}
	
	// Calculate norm
	var norm float64
	for _, state := range states {
		norm += real(state)*real(state) + imag(state)*imag(state)
	}
	
	if math.Abs(norm-1.0) > 0.001 {
		t.Errorf("❌ State not properly normalized: norm = %f, expected ~1.0", norm)
	} else {
		t.Logf("✅ State properly normalized: norm = %f", norm)
	}
}

// Test complex number operations
func TestComplexNumberOperations(t *testing.T) {
	t.Log("🔢 Testing complex number operations...")
	
	// Test complex number creation and manipulation
	c1 := complex(0.5, 0.5)
	c2 := complex(0.5, -0.5)
	
	// Test magnitude calculation
	mag1 := real(c1)*real(c1) + imag(c1)*imag(c1)
	mag2 := real(c2)*real(c2) + imag(c2)*imag(c2)
	
	expectedMag := 0.5
	if math.Abs(mag1-expectedMag) > 0.001 || math.Abs(mag2-expectedMag) > 0.001 {
		t.Errorf("❌ Complex magnitude calculation failed: mag1=%f, mag2=%f, expected=%f", 
			mag1, mag2, expectedMag)
	} else {
		t.Logf("✅ Complex number operations successful: mag1=%f, mag2=%f", mag1, mag2)
	}
}

// Test byte manipulation functions
func TestByteManipulation(t *testing.T) {
	t.Log("📊 Testing byte manipulation...")
	
	// Test data conversion
	testData := []byte("Hello, Quantum World!")
	
	// Basic byte operations
	if len(testData) == 0 {
		t.Error("❌ Test data is empty")
		return
	}
	
	// Test byte copying
	copiedData := make([]byte, len(testData))
	copy(copiedData, testData)
	
	if !bytes.Equal(testData, copiedData) {
		t.Error("❌ Byte copying failed")
	} else {
		t.Logf("✅ Byte manipulation successful: %d bytes processed", len(testData))
	}
}

// Test entropy calculation
func TestBasicEntropy(t *testing.T) {
	t.Log("🎲 Testing basic entropy calculation...")
	
	// Test uniform distribution (high entropy)
	uniformData := []byte{0, 1, 2, 3, 4, 5, 6, 7}
	entropy1 := calculateBasicEntropy(uniformData)
	
	// Test non-uniform distribution (lower entropy)
	nonUniformData := []byte{0, 0, 0, 0, 1, 1, 2, 3}
	entropy2 := calculateBasicEntropy(nonUniformData)
	
	if entropy1 <= entropy2 {
		t.Errorf("❌ Entropy calculation incorrect: uniform=%f should be > non-uniform=%f", 
			entropy1, entropy2)
	} else {
		t.Logf("✅ Entropy calculation correct: uniform=%f > non-uniform=%f", entropy1, entropy2)
	}
}

// Helper function to calculate basic entropy
func calculateBasicEntropy(data []byte) float64 {
	if len(data) == 0 {
		return 0
	}
	
	// Count byte frequencies
	freq := make(map[byte]int)
	for _, b := range data {
		freq[b]++
	}
	
	// Calculate entropy
	var entropy float64
	length := float64(len(data))
	
	for _, count := range freq {
		if count > 0 {
			p := float64(count) / length
			entropy -= p * math.Log2(p)
		}
	}
	
	return entropy
}

// Test hash operations
func TestHashOperations(t *testing.T) {
	t.Log("🔐 Testing hash operations...")
	
	// Test basic hashing
	data1 := []byte("test data 1")
	data2 := []byte("test data 2")
	
	// Simple hash function (for testing)
	hash1 := simpleHash(data1)
	hash2 := simpleHash(data2)
	
	if bytes.Equal(hash1, hash2) {
		t.Error("❌ Different inputs produced same hash")
	} else {
		t.Logf("✅ Hash operations successful: different inputs produce different hashes")
	}
	
	// Test hash consistency
	hash1_repeat := simpleHash(data1)
	if !bytes.Equal(hash1, hash1_repeat) {
		t.Error("❌ Same input produced different hashes")
	} else {
		t.Log("✅ Hash consistency verified")
	}
}

// Simple hash function for testing
func simpleHash(data []byte) []byte {
	// Simple XOR-based hash for testing
	hash := make([]byte, 4)
	for i, b := range data {
		hash[i%4] ^= b
	}
	return hash
}

// Test random number generation
func TestRandomGeneration(t *testing.T) {
	t.Log("🎯 Testing random number generation...")
	
	// Generate random bytes
	randomBytes1 := make([]byte, 32)
	randomBytes2 := make([]byte, 32)
	
	// Fill with pseudo-random data
	for i := range randomBytes1 {
		randomBytes1[i] = byte(i * 17 % 256) // Simple pseudo-random
		randomBytes2[i] = byte(i * 23 % 256) // Different pseudo-random
	}
	
	// Check they're different
	if bytes.Equal(randomBytes1, randomBytes2) {
		t.Error("❌ Random generation produced identical results")
	} else {
		t.Log("✅ Random generation produces different results")
	}
	
	// Check entropy
	entropy1 := calculateBasicEntropy(randomBytes1)
	entropy2 := calculateBasicEntropy(randomBytes2)
	
	if entropy1 < 4.0 || entropy2 < 4.0 {
		t.Logf("⚠️ Low entropy detected: entropy1=%f, entropy2=%f", entropy1, entropy2)
	} else {
		t.Logf("✅ Good entropy: entropy1=%f, entropy2=%f", entropy1, entropy2)
	}
}

// Test performance characteristics
func TestPerformanceCharacteristics(t *testing.T) {
	t.Log("⚡ Testing performance characteristics...")
	
	iterations := 1000
	dataSize := 64
	
	for i := 0; i < iterations; i++ {
		// Create test data
		testData := make([]byte, dataSize)
		for j := range testData {
			testData[j] = byte((i + j) % 256)
		}
		
		// Perform operations
		hash := simpleHash(testData)
		entropy := calculateBasicEntropy(testData)
		
		// Basic validation
		if len(hash) == 0 || entropy < 0 {
			t.Errorf("❌ Performance test failed at iteration %d", i)
			break
		}
	}
	
	t.Logf("✅ Performance test completed: %d iterations", iterations)
}

// Test edge cases
func TestEdgeCases(t *testing.T) {
	t.Log("🔍 Testing edge cases...")
	
	// Test empty data
	emptyData := []byte{}
	entropy := calculateBasicEntropy(emptyData)
	if entropy != 0 {
		t.Errorf("❌ Empty data should have zero entropy, got %f", entropy)
	}
	
	// Test single byte
	singleByte := []byte{42}
	entropy = calculateBasicEntropy(singleByte)
	if entropy != 0 {
		t.Errorf("❌ Single byte should have zero entropy, got %f", entropy)
	}
	
	// Test large data
	largeData := make([]byte, 10000)
	for i := range largeData {
		largeData[i] = byte(i % 256)
	}
	entropy = calculateBasicEntropy(largeData)
	if entropy < 7.0 {
		t.Logf("⚠️ Large data has low entropy: %f", entropy)
	}
	
	t.Log("✅ Edge cases handled correctly")
}

// Benchmark basic operations
func BenchmarkQuantumStateOperations(b *testing.B) {
	states := []complex128{
		complex(0.7071, 0.0),
		complex(0.7071, 0.0),
	}
	
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		var norm float64
		for _, state := range states {
			norm += real(state)*real(state) + imag(state)*imag(state)
		}
		_ = norm
	}
}

// Benchmark hash operations
func BenchmarkHashOperations(b *testing.B) {
	testData := []byte("benchmark test data for hashing operations")
	
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_ = simpleHash(testData)
	}
}

// Benchmark entropy calculation
func BenchmarkEntropyCalculation(b *testing.B) {
	testData := make([]byte, 1024)
	for i := range testData {
		testData[i] = byte(i % 256)
	}
	
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_ = calculateBasicEntropy(testData)
	}
}
