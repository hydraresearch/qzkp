package main

import (
	"testing"
	"math"
	"github.com/hydraresearch/qzkp/src/classical"
	"github.com/hydraresearch/qzkp/src/quantum"
	"github.com/hydraresearch/qzkp/src/security"
)

// Test quantum state creation and normalization
func TestQuantumStateCreation(t *testing.T) {
	t.Log("Testing quantum state creation and normalization...")
	
	// Test basic state creation
	testData := []byte("test quantum state")
	states, err := classical.BytesToState(testData, 4)
	if err != nil {
		t.Fatalf("Failed to create quantum state: %v", err)
	}
	
	// Verify state normalization
	var norm float64
	for _, state := range states {
		norm += real(state)*real(state) + imag(state)*imag(state)
	}
	
	if math.Abs(norm-1.0) > 0.001 {
		t.Errorf("State not properly normalized: norm = %f, expected ~1.0", norm)
	}
	
	t.Logf("✅ Quantum state created with norm: %f", norm)
}

// Test superposition creation
func TestSuperpositionCreation(t *testing.T) {
	t.Log("Testing superposition creation...")
	
	states := []complex128{
		complex(0.5, 0.0),
		complex(0.5, 0.0),
		complex(0.5, 0.0),
		complex(0.5, 0.0),
	}
	
	superpos := classical.CreateSuperposition(states)
	
	if len(superpos.States) != len(states) {
		t.Errorf("Superposition has wrong number of states: got %d, expected %d", 
			len(superpos.States), len(states))
	}
	
	// Test deterministic superposition
	detSuperpos := classical.CreateDeterministicSuperposition(states)
	if len(detSuperpos.States) != len(states) {
		t.Errorf("Deterministic superposition has wrong number of states: got %d, expected %d", 
			len(detSuperpos.States), len(states))
	}
	
	t.Log("✅ Superposition creation successful")
}

// Test commitment generation
func TestCommitmentGeneration(t *testing.T) {
	t.Log("Testing cryptographic commitment generation...")
	
	states := []complex128{
		complex(0.7071, 0.0),
		complex(0.7071, 0.0),
	}
	
	superpos := classical.CreateSuperposition(states)
	key := []byte("test-key-12345678901234567890123456789012") // 32 bytes
	
	commitment := classical.GenerateCommitment(superpos, "test-id", key)
	
	if len(commitment) == 0 {
		t.Error("Commitment generation failed: empty result")
	}
	
	// Test that different inputs produce different commitments
	superpos2 := classical.CreateSuperposition([]complex128{
		complex(0.6, 0.0),
		complex(0.8, 0.0),
	})
	
	commitment2 := classical.GenerateCommitment(superpos2, "test-id-2", key)
	
	if string(commitment) == string(commitment2) {
		t.Error("Different inputs produced identical commitments")
	}
	
	t.Logf("✅ Commitment generation successful, length: %d bytes", len(commitment))
}

// Test quantum safe random generation
func TestQuantumSafeRandom(t *testing.T) {
	t.Log("Testing quantum-safe random number generation...")
	
	qsr, err := classical.NewQuantumSafeRandom()
	if err != nil {
		t.Fatalf("Failed to create quantum safe random: %v", err)
	}
	
	// Generate random bytes
	randomBytes := make([]byte, 32)
	n, err := qsr.Read(randomBytes)
	if err != nil {
		t.Fatalf("Failed to generate random bytes: %v", err)
	}
	
	if n != 32 {
		t.Errorf("Expected 32 random bytes, got %d", n)
	}
	
	// Test randomness validation
	metrics := classical.ValidateRandomness(randomBytes)
	
	if len(metrics) == 0 {
		t.Error("Randomness validation returned no metrics")
	}
	
	t.Logf("✅ Quantum-safe random generation successful, metrics: %v", metrics)
}

// Test secure quantum ZKP creation
func TestSecureQuantumZKP(t *testing.T) {
	t.Log("Testing secure quantum ZKP creation...")
	
	ctx := []byte("test-context")
	zkp, err := security.NewSecureQuantumZKP(4, 128, ctx)
	if err != nil {
		t.Fatalf("Failed to create secure quantum ZKP: %v", err)
	}
	
	if zkp == nil {
		t.Error("Secure quantum ZKP creation returned nil")
	}
	
	// Test ultra-secure variant
	ultraZkp, err := security.NewUltraSecureQuantumZKP(4, 256, ctx)
	if err != nil {
		t.Fatalf("Failed to create ultra-secure quantum ZKP: %v", err)
	}
	
	if ultraZkp == nil {
		t.Error("Ultra-secure quantum ZKP creation returned nil")
	}
	
	t.Log("✅ Secure quantum ZKP creation successful")
}

// Test encoding edge cases
func TestEncodingEdgeCases(t *testing.T) {
	t.Log("Testing encoding edge cases...")
	
	// Test empty data
	_, err := classical.BytesToState([]byte{}, 4)
	if err == nil {
		t.Error("Expected error for empty data, got nil")
	}
	
	// Test very small target size
	_, err = classical.BytesToState([]byte("test"), 1)
	if err != nil {
		t.Errorf("Unexpected error for small target size: %v", err)
	}
	
	// Test large data
	largeData := make([]byte, 1024)
	for i := range largeData {
		largeData[i] = byte(i % 256)
	}
	
	states, err := classical.BytesToState(largeData, 16)
	if err != nil {
		t.Errorf("Failed to encode large data: %v", err)
	}
	
	if len(states) != 16 {
		t.Errorf("Expected 16 states, got %d", len(states))
	}
	
	t.Log("✅ Encoding edge cases handled correctly")
}

// Test performance characteristics
func TestPerformanceCharacteristics(t *testing.T) {
	t.Log("Testing performance characteristics...")
	
	// Test multiple iterations for consistency
	iterations := 100
	var totalNorm float64
	
	for i := 0; i < iterations; i++ {
		testData := []byte("performance test data")
		states, err := classical.BytesToState(testData, 8)
		if err != nil {
			t.Fatalf("Performance test failed at iteration %d: %v", i, err)
		}
		
		var norm float64
		for _, state := range states {
			norm += real(state)*real(state) + imag(state)*imag(state)
		}
		totalNorm += norm
	}
	
	avgNorm := totalNorm / float64(iterations)
	if math.Abs(avgNorm-1.0) > 0.01 {
		t.Errorf("Average normalization inconsistent: %f", avgNorm)
	}
	
	t.Logf("✅ Performance test completed: %d iterations, avg norm: %f", iterations, avgNorm)
}

// Benchmark quantum state creation
func BenchmarkQuantumStateCreation(b *testing.B) {
	testData := []byte("benchmark test data for quantum state creation")
	
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_, err := classical.BytesToState(testData, 8)
		if err != nil {
			b.Fatalf("Benchmark failed: %v", err)
		}
	}
}

// Benchmark commitment generation
func BenchmarkCommitmentGeneration(b *testing.B) {
	states := []complex128{
		complex(0.7071, 0.0),
		complex(0.7071, 0.0),
	}
	superpos := classical.CreateSuperposition(states)
	key := []byte("benchmark-key-1234567890123456789012345678")
	
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		classical.GenerateCommitment(superpos, "bench-id", key)
	}
}
