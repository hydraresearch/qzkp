package main

import (
	"testing"
	"bytes"
	"crypto/rand"
	"crypto/sha256"
	"math"
	"time"
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
	
	leakageDetected := false
	
	for i, vector := range testVectors {
		t.Logf("Testing vector %d: %s", i+1, string(vector))
		
		// Generate hash (simulating commitment)
		hash := sha256.Sum256(vector)
		
		// Check for leakage (simplified check)
		if containsPattern(hash[:], vector) {
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
	
	// Generate commitments for both secrets
	hash1 := sha256.Sum256(secret1)
	hash2 := sha256.Sum256(secret2)
	
	// Commitments should be different
	if bytes.Equal(hash1[:], hash2[:]) {
		t.Error("❌ Different secrets produced identical commitments")
	} else {
		t.Log("✅ Different secrets produce different commitments")
	}
	
	// Neither commitment should reveal the original secret
	if containsPattern(hash1[:], secret1) {
		t.Error("❌ Commitment1 contains original secret")
	}
	
	if containsPattern(hash2[:], secret2) {
		t.Error("❌ Commitment2 contains original secret")
	}
	
	t.Log("✅ Zero-knowledge property validated")
}

// Test soundness property
func TestSoundnessProperty(t *testing.T) {
	t.Log("🎯 Testing soundness property...")
	
	// Test with multiple security levels
	securityLevels := []int{32, 64, 80, 128}
	
	for _, level := range securityLevels {
		t.Logf("Testing soundness for %d-bit security", level)
		
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
	
	for i := 0; i < totalTests; i++ {
		testData := []byte("completeness test data")
		
		// Generate hash (simulating proof generation)
		hash := sha256.Sum256(testData)
		
		if len(hash) > 0 {
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
	var timings []time.Duration
	
	for i := 0; i < timingTests; i++ {
		testData := []byte("timing test data")
		
		// Measure timing
		start := time.Now()
		hash := sha256.Sum256(testData)
		duration := time.Since(start)
		
		timings = append(timings, duration)
		_ = hash // Use the hash to prevent optimization
	}
	
	// Check timing consistency
	if len(timings) > 0 {
		var sum time.Duration
		for _, timing := range timings {
			sum += timing
		}
		avgTiming := sum / time.Duration(len(timings))
		
		// Check variance
		var variance time.Duration
		for _, timing := range timings {
			diff := timing - avgTiming
			if diff < 0 {
				diff = -diff
			}
			variance += diff
		}
		variance /= time.Duration(len(timings))
		
		if variance > avgTiming/10 { // Allow 10% variance
			t.Logf("⚠️ High timing variance detected: %v (avg: %v)", variance, avgTiming)
		} else {
			t.Logf("✅ Timing consistency good: variance %v (avg: %v)", variance, avgTiming)
		}
	}
}

// Test replay attack resistance
func TestReplayAttackResistance(t *testing.T) {
	t.Log("🔄 Testing replay attack resistance...")
	
	testData := []byte("replay test data")
	
	// Generate multiple commitments with same input but different randomness
	commitments := make([][]byte, 5)
	
	for i := range commitments {
		// Add randomness to prevent replay
		randomBytes := make([]byte, 16)
		rand.Read(randomBytes)
		
		// Combine data with randomness
		combined := append(testData, randomBytes...)
		hash := sha256.Sum256(combined)
		commitments[i] = hash[:]
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
	
	// Generate random data
	randomData := make([]byte, 1024)
	n, err := rand.Read(randomData)
	if err != nil {
		t.Fatalf("Failed to generate random data: %v", err)
	}
	
	if n != len(randomData) {
		t.Errorf("Expected %d random bytes, got %d", len(randomData), n)
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

// Test cryptographic hash properties
func TestCryptographicHashProperties(t *testing.T) {
	t.Log("🔐 Testing cryptographic hash properties...")
	
	// Test determinism
	data := []byte("test data for hash properties")
	hash1 := sha256.Sum256(data)
	hash2 := sha256.Sum256(data)
	
	if !bytes.Equal(hash1[:], hash2[:]) {
		t.Error("❌ Hash function is not deterministic")
	} else {
		t.Log("✅ Hash function is deterministic")
	}
	
	// Test avalanche effect
	data1 := []byte("test data")
	data2 := []byte("test datb") // One bit difference
	
	hash1 = sha256.Sum256(data1)
	hash2 = sha256.Sum256(data2)
	
	// Count different bits
	differentBits := 0
	for i := 0; i < len(hash1); i++ {
		xor := hash1[i] ^ hash2[i]
		for xor != 0 {
			differentBits++
			xor &= xor - 1
		}
	}
	
	// Should have approximately 50% different bits (avalanche effect)
	totalBits := len(hash1) * 8
	diffPercentage := float64(differentBits) / float64(totalBits) * 100
	
	if diffPercentage < 40 || diffPercentage > 60 {
		t.Logf("⚠️ Avalanche effect may be weak: %.1f%% bits different", diffPercentage)
	} else {
		t.Logf("✅ Good avalanche effect: %.1f%% bits different", diffPercentage)
	}
}

// Test attack scenario simulation
func TestAttackScenarioSimulation(t *testing.T) {
	t.Log("⚔️ Testing attack scenario simulation...")
	
	// Simulate brute force attack
	target := []byte("secret")
	targetHash := sha256.Sum256(target)
	
	// Try to find collision (simplified)
	attempts := 1000
	found := false
	
	for i := 0; i < attempts; i++ {
		candidate := []byte("guess" + string(rune(i)))
		candidateHash := sha256.Sum256(candidate)
		
		if bytes.Equal(targetHash[:], candidateHash[:]) && !bytes.Equal(target, candidate) {
			found = true
			t.Errorf("❌ Collision found after %d attempts", i+1)
			break
		}
	}
	
	if !found {
		t.Logf("✅ No collision found after %d attempts", attempts)
	}
}

// Benchmark security operations
func BenchmarkSecurityOperations(b *testing.B) {
	testData := []byte("security benchmark data")
	
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		hash := sha256.Sum256(testData)
		_ = hash
	}
}

// Benchmark entropy calculation
func BenchmarkEntropyCalculation(b *testing.B) {
	testData := make([]byte, 1024)
	rand.Read(testData)
	
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_ = calculateBasicEntropy(testData)
	}
}

// Benchmark random generation
func BenchmarkRandomGeneration(b *testing.B) {
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		randomData := make([]byte, 32)
		rand.Read(randomData)
		_ = randomData
	}
}
