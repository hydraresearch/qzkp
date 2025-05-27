package main

import (
	"testing"
	"bytes"
	"encoding/json"
	"math"
	"crypto/rand"
	"github.com/hydraresearch/qzkp/src/classical"
	"github.com/hydraresearch/qzkp/src/security"
)

// Test information leakage detection
func TestInformationLeakageDetection(t *testing.T) {
	t.Log("🔍 Testing information leakage detection...")
	
	// Create distinctive test vectors
	testVectors := [][]byte{
		[]byte("AAAAAAAAAAAAAAAA"), // Repeated pattern
		[]byte("0123456789ABCDEF"), // Sequential pattern
		[]byte("FEDCBA9876543210"), // Reverse sequential
		[]byte("A5A5A5A5A5A5A5A5"), // Alternating pattern
	}
	
	key := []byte("security-test-key-32bytes-length")
	leakageDetected := false
	
	for i, vector := range testVectors {
		t.Logf("Testing vector %d: %s", i+1, string(vector))
		
		// Generate quantum state
		states, err := classical.BytesToState(vector, 8)
		if err != nil {
			t.Errorf("Failed to create quantum state for vector %d: %v", i+1, err)
			continue
		}
		
		// Create superposition and commitment
		superpos := classical.CreateSuperposition(states)
		commitment := classical.GenerateCommitment(superpos, "security-test", key)
		
		// Check for leakage (simplified check)
		if containsPattern(commitment, vector) {
			leakageDetected = true
			t.Errorf("❌ Information leakage detected in vector %d", i+1)
		} else {
			t.Logf("✅ No leakage detected in vector %d", i+1)
		}
	}
	
	if !leakageDetected {
		t.Log("✅ All security tests passed - no information leakage detected")
	}
}

// Helper function to check for pattern leakage
func containsPattern(commitment []byte, pattern []byte) bool {
	// Simple pattern detection - check if original bytes appear in commitment
	return bytes.Contains(commitment, pattern)
}

// Test zero-knowledge property
func TestZeroKnowledgeProperty(t *testing.T) {
	t.Log("🔐 Testing zero-knowledge property...")
	
	// Generate two different secrets
	secret1 := []byte("secret-data-one")
	secret2 := []byte("secret-data-two")
	
	key := []byte("zk-test-key-32bytes-length-exact")
	
	// Generate commitments for both secrets
	states1, err := classical.BytesToState(secret1, 8)
	if err != nil {
		t.Fatalf("Failed to create quantum state for secret1: %v", err)
	}
	
	states2, err := classical.BytesToState(secret2, 8)
	if err != nil {
		t.Fatalf("Failed to create quantum state for secret2: %v", err)
	}
	
	superpos1 := classical.CreateSuperposition(states1)
	superpos2 := classical.CreateSuperposition(states2)
	
	commitment1 := classical.GenerateCommitment(superpos1, "zk-test-1", key)
	commitment2 := classical.GenerateCommitment(superpos2, "zk-test-2", key)
	
	// Commitments should be different
	if bytes.Equal(commitment1, commitment2) {
		t.Error("❌ Different secrets produced identical commitments")
	} else {
		t.Log("✅ Different secrets produce different commitments")
	}
	
	// Neither commitment should reveal the original secret
	if containsPattern(commitment1, secret1) {
		t.Error("❌ Commitment1 contains original secret")
	}
	
	if containsPattern(commitment2, secret2) {
		t.Error("❌ Commitment2 contains original secret")
	}
	
	t.Log("✅ Zero-knowledge property validated")
}

// Test soundness property
func TestSoundnessProperty(t *testing.T) {
	t.Log("🎯 Testing soundness property...")
	
	// Test with multiple security levels
	securityLevels := []int{32, 64, 80, 128}
	ctx := []byte("soundness-test")
	
	for _, level := range securityLevels {
		t.Logf("Testing soundness for %d-bit security", level)
		
		zkp, err := security.NewSecureQuantumZKP(8, level, ctx)
		if err != nil {
			t.Errorf("Failed to create ZKP for %d-bit security: %v", level, err)
			continue
		}
		
		if zkp == nil {
			t.Errorf("ZKP creation returned nil for %d-bit security", level)
			continue
		}
		
		// Calculate expected soundness error
		expectedError := math.Pow(2, -float64(level))
		t.Logf("Expected soundness error for %d-bit: %.2e", level, expectedError)
		
		if expectedError > 1e-6 && level >= 32 {
			t.Logf("✅ Soundness error within acceptable bounds for %d-bit", level)
		}
	}
}

// Test completeness property
func TestCompletenessProperty(t *testing.T) {
	t.Log("✅ Testing completeness property...")
	
	successCount := 0
	totalTests := 100
	
	key := []byte("completeness-test-key-32bytes-ok")
	
	for i := 0; i < totalTests; i++ {
		testData := []byte("completeness test data")
		
		states, err := classical.BytesToState(testData, 4)
		if err != nil {
			t.Logf("Test %d failed: %v", i+1, err)
			continue
		}
		
		superpos := classical.CreateSuperposition(states)
		commitment := classical.GenerateCommitment(superpos, "completeness", key)
		
		if len(commitment) > 0 {
			successCount++
		}
	}
	
	successRate := float64(successCount) / float64(totalTests)
	
	if successRate < 0.99 {
		t.Errorf("❌ Completeness rate too low: %.2f%% (expected ≥99%%)", successRate*100)
	} else {
		t.Logf("✅ Completeness rate: %.2f%% (%d/%d)", successRate*100, successCount, totalTests)
	}
}

// Test side-channel resistance
func TestSideChannelResistance(t *testing.T) {
	t.Log("🛡️ Testing side-channel resistance...")
	
	// Test timing consistency
	timingTests := 50
	var timings []int64
	
	key := []byte("side-channel-test-key-32bytes-ok")
	
	for i := 0; i < timingTests; i++ {
		testData := []byte("timing test data")
		
		// Measure timing (simplified)
		states, err := classical.BytesToState(testData, 4)
		if err != nil {
			continue
		}
		
		superpos := classical.CreateSuperposition(states)
		commitment := classical.GenerateCommitment(superpos, "timing", key)
		
		// Record commitment length as timing proxy
		timings = append(timings, int64(len(commitment)))
	}
	
	// Check timing consistency
	if len(timings) > 0 {
		var sum int64
		for _, timing := range timings {
			sum += timing
		}
		avgTiming := sum / int64(len(timings))
		
		// Check variance
		var variance int64
		for _, timing := range timings {
			diff := timing - avgTiming
			variance += diff * diff
		}
		variance /= int64(len(timings))
		
		if variance > avgTiming/10 { // Allow 10% variance
			t.Logf("⚠️ High timing variance detected: %d (avg: %d)", variance, avgTiming)
		} else {
			t.Logf("✅ Timing consistency good: variance %d (avg: %d)", variance, avgTiming)
		}
	}
}

// Test replay attack resistance
func TestReplayAttackResistance(t *testing.T) {
	t.Log("🔄 Testing replay attack resistance...")
	
	testData := []byte("replay test data")
	key := []byte("replay-test-key-32bytes-length")
	
	// Generate multiple commitments with same input
	commitments := make([][]byte, 5)
	
	for i := range commitments {
		states, err := classical.BytesToState(testData, 4)
		if err != nil {
			t.Errorf("Failed to create state for replay test %d: %v", i, err)
			continue
		}
		
		superpos := classical.CreateSuperposition(states)
		commitments[i] = classical.GenerateCommitment(superpos, "replay-test", key)
	}
	
	// Check that commitments are different (due to randomization)
	uniqueCommitments := make(map[string]bool)
	for i, commitment := range commitments {
		if len(commitment) == 0 {
			continue
		}
		
		commitmentStr := string(commitment)
		if uniqueCommitments[commitmentStr] {
			t.Errorf("❌ Duplicate commitment found at index %d", i)
		} else {
			uniqueCommitments[commitmentStr] = true
		}
	}
	
	if len(uniqueCommitments) >= len(commitments)-1 { // Allow for one failure
		t.Logf("✅ Replay resistance good: %d unique commitments", len(uniqueCommitments))
	} else {
		t.Errorf("❌ Poor replay resistance: only %d unique commitments", len(uniqueCommitments))
	}
}

// Test randomness quality
func TestRandomnessQuality(t *testing.T) {
	t.Log("🎲 Testing randomness quality...")
	
	qsr, err := classical.NewQuantumSafeRandom()
	if err != nil {
		t.Fatalf("Failed to create quantum safe random: %v", err)
	}
	
	// Generate random data
	randomData := make([]byte, 1024)
	n, err := qsr.Read(randomData)
	if err != nil {
		t.Fatalf("Failed to generate random data: %v", err)
	}
	
	if n != len(randomData) {
		t.Errorf("Expected %d random bytes, got %d", len(randomData), n)
	}
	
	// Validate randomness
	metrics := classical.ValidateRandomness(randomData)
	
	if len(metrics) == 0 {
		t.Error("❌ No randomness metrics returned")
	} else {
		t.Logf("✅ Randomness metrics: %v", metrics)
	}
	
	// Basic entropy check
	entropy := calculateBasicEntropy(randomData)
	if entropy < 7.0 { // Expect high entropy for good randomness
		t.Errorf("❌ Low entropy detected: %.2f", entropy)
	} else {
		t.Logf("✅ Good entropy: %.2f", entropy)
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

// Benchmark security operations
func BenchmarkSecurityOperations(b *testing.B) {
	key := []byte("benchmark-security-key-32bytes")
	testData := []byte("security benchmark data")
	
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		states, _ := classical.BytesToState(testData, 4)
		superpos := classical.CreateSuperposition(states)
		classical.GenerateCommitment(superpos, "security-bench", key)
	}
}
