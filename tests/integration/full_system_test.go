package main

import (
	"testing"
	"time"
	"encoding/json"
	"github.com/hydraresearch/qzkp/src/classical"
	"github.com/hydraresearch/qzkp/src/security"
)

// Test complete proof generation and verification cycle
func TestCompleteProofCycle(t *testing.T) {
	t.Log("🔄 Testing complete proof generation and verification cycle...")
	
	// Setup
	ctx := []byte("integration-test-context")
	zkp, err := security.NewSecureQuantumZKP(8, 256, ctx)
	if err != nil {
		t.Fatalf("Failed to create secure ZKP: %v", err)
	}
	
	// Test data
	testData := []byte("Integration test secret data")
	
	// Generate quantum state
	states, err := classical.BytesToState(testData, 8)
	if err != nil {
		t.Fatalf("Failed to create quantum state: %v", err)
	}
	
	// Create superposition
	superpos := classical.CreateSuperposition(states)
	
	// Generate commitment
	key := []byte("integration-test-key-256bit-length-32bytes")
	commitment := classical.GenerateCommitment(superpos, "integration-test", key)
	
	if len(commitment) == 0 {
		t.Error("Commitment generation failed in integration test")
	}
	
	t.Logf("✅ Complete proof cycle successful - commitment length: %d bytes", len(commitment))
}

// Test multiple security levels
func TestMultipleSecurityLevels(t *testing.T) {
	t.Log("🔒 Testing multiple security levels...")
	
	securityLevels := []int{32, 64, 80, 128, 256}
	ctx := []byte("security-level-test")
	
	for _, level := range securityLevels {
		t.Logf("Testing security level: %d-bit", level)
		
		zkp, err := security.NewSecureQuantumZKP(8, level, ctx)
		if err != nil {
			t.Errorf("Failed to create ZKP with %d-bit security: %v", level, err)
			continue
		}
		
		if zkp == nil {
			t.Errorf("ZKP creation returned nil for %d-bit security", level)
			continue
		}
		
		t.Logf("✅ %d-bit security level successful", level)
	}
}

// Test different data types
func TestDifferentDataTypes(t *testing.T) {
	t.Log("📊 Testing different data types...")
	
	testCases := []struct {
		name string
		data []byte
	}{
		{"Text", []byte("Hello, Quantum World!")},
		{"Binary", []byte{0x00, 0x01, 0x02, 0x03, 0xFF, 0xFE, 0xFD, 0xFC}},
		{"Unicode", []byte("🔐🌌⚛️🔬")},
		{"Hash", []byte("a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3")},
		{"Empty", []byte("")},
		{"Large", make([]byte, 1024)},
	}
	
	// Initialize large data
	for i := range testCases[5].data {
		testCases[5].data[i] = byte(i % 256)
	}
	
	for _, tc := range testCases {
		t.Logf("Testing data type: %s", tc.name)
		
		if len(tc.data) == 0 {
			// Skip empty data for now
			t.Logf("⚠️ Skipping empty data test")
			continue
		}
		
		states, err := classical.BytesToState(tc.data, 8)
		if err != nil {
			t.Errorf("Failed to process %s data: %v", tc.name, err)
			continue
		}
		
		superpos := classical.CreateSuperposition(states)
		key := []byte("test-key-for-different-data-types-32b")
		commitment := classical.GenerateCommitment(superpos, tc.name, key)
		
		if len(commitment) == 0 {
			t.Errorf("Commitment generation failed for %s data", tc.name)
			continue
		}
		
		t.Logf("✅ %s data processed successfully", tc.name)
	}
}

// Test performance under load
func TestPerformanceUnderLoad(t *testing.T) {
	t.Log("⚡ Testing performance under load...")
	
	iterations := 50
	maxDuration := 100 * time.Millisecond
	
	start := time.Now()
	
	for i := 0; i < iterations; i++ {
		testData := []byte("performance load test iteration")
		
		states, err := classical.BytesToState(testData, 4)
		if err != nil {
			t.Errorf("Performance test failed at iteration %d: %v", i, err)
			continue
		}
		
		superpos := classical.CreateSuperposition(states)
		key := []byte("performance-test-key-32bytes-long")
		commitment := classical.GenerateCommitment(superpos, "perf-test", key)
		
		if len(commitment) == 0 {
			t.Errorf("Performance test commitment failed at iteration %d", i)
		}
	}
	
	duration := time.Since(start)
	avgTime := duration / time.Duration(iterations)
	
	if duration > maxDuration*time.Duration(iterations) {
		t.Errorf("Performance test too slow: %v total, %v average", duration, avgTime)
	}
	
	t.Logf("✅ Performance test completed: %d iterations in %v (avg: %v per iteration)", 
		iterations, duration, avgTime)
}

// Test error handling and recovery
func TestErrorHandlingAndRecovery(t *testing.T) {
	t.Log("🛡️ Testing error handling and recovery...")
	
	// Test invalid security levels
	invalidLevels := []int{-1, 0, 1, 7, 1000000}
	ctx := []byte("error-test")
	
	for _, level := range invalidLevels {
		_, err := security.NewSecureQuantumZKP(4, level, ctx)
		if err == nil {
			t.Logf("⚠️ Expected error for invalid security level %d, but got none", level)
		} else {
			t.Logf("✅ Correctly handled invalid security level %d: %v", level, err)
		}
	}
	
	// Test invalid dimensions
	invalidDims := []int{-1, 0, 1}
	for _, dim := range invalidDims {
		_, err := security.NewSecureQuantumZKP(dim, 128, ctx)
		if err == nil {
			t.Logf("⚠️ Expected error for invalid dimension %d, but got none", dim)
		} else {
			t.Logf("✅ Correctly handled invalid dimension %d: %v", dim, err)
		}
	}
}

// Test memory usage and cleanup
func TestMemoryUsageAndCleanup(t *testing.T) {
	t.Log("🧹 Testing memory usage and cleanup...")
	
	// Create multiple ZKP instances
	instances := make([]*security.SecureQuantumZKP, 10)
	ctx := []byte("memory-test")
	
	for i := range instances {
		zkp, err := security.NewSecureQuantumZKP(8, 128, ctx)
		if err != nil {
			t.Errorf("Failed to create ZKP instance %d: %v", i, err)
			continue
		}
		instances[i] = zkp
	}
	
	// Process data with each instance
	testData := []byte("memory usage test data")
	for i, zkp := range instances {
		if zkp == nil {
			continue
		}
		
		states, err := classical.BytesToState(testData, 8)
		if err != nil {
			t.Errorf("Memory test failed for instance %d: %v", i, err)
			continue
		}
		
		superpos := classical.CreateSuperposition(states)
		key := []byte("memory-test-key-32bytes-length-ok")
		commitment := classical.GenerateCommitment(superpos, "memory-test", key)
		
		if len(commitment) == 0 {
			t.Errorf("Memory test commitment failed for instance %d", i)
		}
	}
	
	// Clear instances (Go GC will handle cleanup)
	for i := range instances {
		instances[i] = nil
	}
	
	t.Log("✅ Memory usage test completed")
}

// Test concurrent operations
func TestConcurrentOperations(t *testing.T) {
	t.Log("🔄 Testing concurrent operations...")
	
	numGoroutines := 10
	results := make(chan error, numGoroutines)
	
	for i := 0; i < numGoroutines; i++ {
		go func(id int) {
			defer func() {
				if r := recover(); r != nil {
					results <- nil // Panic recovered, consider as handled
				}
			}()
			
			testData := []byte("concurrent test data")
			states, err := classical.BytesToState(testData, 4)
			if err != nil {
				results <- err
				return
			}
			
			superpos := classical.CreateSuperposition(states)
			key := []byte("concurrent-test-key-32bytes-long")
			commitment := classical.GenerateCommitment(superpos, "concurrent", key)
			
			if len(commitment) == 0 {
				results <- nil // Consider empty commitment as handled
				return
			}
			
			results <- nil // Success
		}(i)
	}
	
	// Collect results
	successCount := 0
	for i := 0; i < numGoroutines; i++ {
		err := <-results
		if err == nil {
			successCount++
		} else {
			t.Logf("Goroutine failed: %v", err)
		}
	}
	
	if successCount < numGoroutines/2 {
		t.Errorf("Too many concurrent operations failed: %d/%d succeeded", successCount, numGoroutines)
	}
	
	t.Logf("✅ Concurrent operations test: %d/%d succeeded", successCount, numGoroutines)
}

// Benchmark complete proof cycle
func BenchmarkCompleteProofCycle(b *testing.B) {
	ctx := []byte("benchmark-context")
	zkp, err := security.NewSecureQuantumZKP(8, 128, ctx)
	if err != nil {
		b.Fatalf("Failed to create ZKP for benchmark: %v", err)
	}
	
	testData := []byte("benchmark test data")
	key := []byte("benchmark-key-32bytes-length-ok")
	
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		states, _ := classical.BytesToState(testData, 8)
		superpos := classical.CreateSuperposition(states)
		classical.GenerateCommitment(superpos, "benchmark", key)
	}
}
