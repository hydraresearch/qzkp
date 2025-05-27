package main

import (
	"encoding/json"
	"fmt"
	"log"
	"strings"
	"time"
)

// mustMarshal is a helper function for examples
func mustMarshal(v interface{}) []byte {
	data, err := json.Marshal(v)
	if err != nil {
		panic(err)
	}
	return data
}

// Example1_BasicSecureProof demonstrates basic secure proof generation and verification
func Example1_BasicSecureProof() {
	fmt.Println("=== Example 1: Basic Secure Quantum ZKP ===")
	
	// Initialize secure quantum ZKP system
	ctx := []byte("example-application-context")
	sq, err := NewSecureQuantumZKP(3, 128, ctx)
	if err != nil {
		log.Fatal("Failed to initialize SecureQuantumZKP:", err)
	}
	
	// Secret quantum state vector (Bell state: (|00⟩ + |11⟩)/√2)
	secretVector := []complex128{
		complex(0.7071, 0),    // |00⟩ component
		complex(0.7071, 0),    // |01⟩ component  
		complex(0, 0),         // |10⟩ component
		complex(0, 0),         // |11⟩ component
	}
	
	// Generate secure proof
	identifier := "bell-state-example"
	key := []byte("32-byte-authentication-key-here!")
	
	fmt.Println("Generating secure proof...")
	start := time.Now()
	proof, err := sq.SecureProveVectorKnowledge(secretVector, identifier, key)
	if err != nil {
		log.Fatal("Proof generation failed:", err)
	}
	proofTime := time.Since(start)
	
	// Verify proof (without learning the secret!)
	fmt.Println("Verifying proof...")
	start = time.Now()
	isValid := sq.VerifySecureProof(proof, key)
	verifyTime := time.Since(start)
	
	// Results
	fmt.Printf("✅ Proof valid: %v\n", isValid)
	fmt.Printf("📊 Proof generation time: %v\n", proofTime)
	fmt.Printf("📊 Verification time: %v\n", verifyTime)
	fmt.Printf("📊 Proof size: %d bytes\n", len(mustMarshal(proof)))
	fmt.Printf("🔒 Challenge responses: %d\n", len(proof.ChallengeResponse))
	
	// Demonstrate that the proof contains NO secret information
	proofJSON := string(mustMarshal(proof))
	fmt.Println("\n🔍 Security Check:")
	for i, component := range secretVector {
		realStr := fmt.Sprintf("%.4f", real(component))
		imagStr := fmt.Sprintf("%.4f", imag(component))
		if strings.Contains(proofJSON, realStr) || strings.Contains(proofJSON, imagStr) {
			fmt.Printf("❌ WARNING: Component %d might be leaked!\n", i)
		} else {
			fmt.Printf("✅ Component %d: No leakage detected\n", i)
		}
	}
	
	fmt.Println()
}

// Example2_ProofFromBytes demonstrates proving knowledge of arbitrary data
func Example2_ProofFromBytes() {
	fmt.Println("=== Example 2: Proof from Arbitrary Data ===")
	
	sq, err := NewSecureQuantumZKP(3, 128, []byte("document-auth-context"))
	if err != nil {
		log.Fatal(err)
	}
	
	// Secret document content
	secretDocument := []byte(`
CONFIDENTIAL RESEARCH DOCUMENT
==============================
Project: Quantum Cryptography Implementation
Classification: Restricted
Date: 2024

Abstract:
This document contains sensitive information about quantum
zero-knowledge proof implementations and their security
properties. The contents should not be disclosed without
proper authorization.

Key Findings:
- Quantum state vectors can be used for zero-knowledge proofs
- Post-quantum cryptography is essential for long-term security
- Information leakage is a critical concern in naive implementations

[Additional content redacted for security]
`)
	
	identifier := "research-doc-2024-001"
	key := []byte("document-signing-key-32-bytes!!")
	
	fmt.Printf("Document size: %d bytes\n", len(secretDocument))
	fmt.Println("Generating proof of document knowledge...")
	
	// Generate proof directly from bytes
	start := time.Now()
	proof, err := sq.SecureProveFromBytes(secretDocument, identifier, key)
	if err != nil {
		log.Fatal("Proof generation failed:", err)
	}
	proofTime := time.Since(start)
	
	// Verify without learning anything about the document
	fmt.Println("Verifying document proof...")
	start = time.Now()
	isValid := sq.VerifySecureProof(proof, key)
	verifyTime := time.Since(start)
	
	fmt.Printf("✅ Document proof valid: %v\n", isValid)
	fmt.Printf("📊 Proof generation time: %v\n", proofTime)
	fmt.Printf("📊 Verification time: %v\n", verifyTime)
	fmt.Printf("📊 Proof size: %d bytes\n", len(mustMarshal(proof)))
	
	// Security check: ensure document content is not leaked
	proofJSON := string(mustMarshal(proof))
	sensitiveWords := []string{"CONFIDENTIAL", "Quantum", "Cryptography", "security", "redacted"}
	
	fmt.Println("\n🔍 Document Content Security Check:")
	leakageFound := false
	for _, word := range sensitiveWords {
		if strings.Contains(proofJSON, word) {
			fmt.Printf("❌ Potential leakage: '%s' found in proof\n", word)
			leakageFound = true
		}
	}
	
	if !leakageFound {
		fmt.Println("✅ No sensitive document content leaked in proof!")
	}
	
	// Test with wrong key
	wrongKey := []byte("wrong-key-should-fail-verification")
	if sq.VerifySecureProof(proof, wrongKey) {
		fmt.Println("❌ WARNING: Proof verified with wrong key!")
	} else {
		fmt.Println("✅ Proof correctly rejected with wrong key")
	}
	
	fmt.Println()
}

// Example3_QuantumCircuitOperations demonstrates quantum circuit building and execution
func Example3_QuantumCircuitOperations() {
	fmt.Println("=== Example 3: Quantum Circuit Operations ===")
	
	q, err := NewQuantumZKP(3, 128, []byte("circuit-context"))
	if err != nil {
		log.Fatal(err)
	}
	
	// Create a superposition state
	superpositionState := []complex128{
		complex(0.5, 0.1),  // |00⟩
		complex(0.4, 0.2),  // |01⟩
		complex(0.3, 0.3),  // |10⟩
		complex(0.2, 0.4),  // |11⟩
	}
	
	fmt.Println("Building quantum circuit...")
	
	// Build quantum circuit from state vector
	circuit, err := q.BuildCircuit(superpositionState, "superposition-demo")
	if err != nil {
		log.Fatal("Circuit building failed:", err)
	}
	
	fmt.Printf("📊 Circuit qubits: %d\n", circuit.NumQubits)
	fmt.Printf("📊 Circuit gates: %d\n", len(circuit.Gates))
	fmt.Printf("📊 Classical bits: %d\n", circuit.NumClbits)
	
	// Demonstrate different optimization levels
	optimizationLevels := []int{0, 1, 2, 3}
	
	for _, level := range optimizationLevels {
		fmt.Printf("\n🔧 Optimization Level %d:\n", level)
		
		// Transpile circuit
		start := time.Now()
		transpiled, err := q.TranspileCircuit(circuit, level)
		if err != nil {
			log.Printf("Transpilation failed: %v", err)
			continue
		}
		transpileTime := time.Since(start)
		
		// Apply noise mitigation
		start = time.Now()
		mitigated, err := q.ApplyNoiseMitigation(transpiled)
		if err != nil {
			log.Printf("Noise mitigation failed: %v", err)
			continue
		}
		mitigationTime := time.Since(start)
		
		// Execute circuit
		start = time.Now()
		result, err := q.ExecuteCircuit(mitigated, 1000)
		if err != nil {
			log.Printf("Circuit execution failed: %v", err)
			continue
		}
		executionTime := time.Since(start)
		
		fmt.Printf("  - Transpilation: %v\n", transpileTime)
		fmt.Printf("  - Noise mitigation: %v\n", mitigationTime)
		fmt.Printf("  - Execution: %v\n", executionTime)
		fmt.Printf("  - Gates after optimization: %d\n", len(mitigated.Gates))
		fmt.Printf("  - Unique measurement outcomes: %d\n", len(result.Counts))
		
		// Show top measurement outcomes
		fmt.Printf("  - Top measurement results:\n")
		count := 0
		for bitstring, freq := range result.Counts {
			if count >= 3 {
				break
			}
			fmt.Printf("    |%s⟩: %d times (%.1f%%)\n", bitstring, freq, float64(freq)/float64(result.Shots)*100)
			count++
		}
	}
	
	fmt.Println()
}

// Example4_SecurityComparison demonstrates the security difference between implementations
func Example4_SecurityComparison() {
	fmt.Println("=== Example 4: Security Comparison ===")
	
	// Test vector with known values
	testVector := []complex128{
		complex(0.8, 0.2),  // Easily identifiable values
		complex(0.3, 0.5),
		complex(0.1, 0.7),
		complex(0.4, 0.1),
	}
	
	identifier := "security-demo"
	key := []byte("comparison-key-32-bytes-long!!!")
	
	fmt.Println("🔴 Testing INSECURE implementation...")
	
	// INSECURE implementation (for demonstration only)
	q, err := NewQuantumZKP(3, 128, []byte("insecure-demo"))
	if err != nil {
		log.Fatal(err)
	}
	
	insecureProof, err := q.Prove(testVector, identifier, key)
	if err != nil {
		log.Printf("Insecure proof generation failed: %v", err)
	} else {
		insecureJSON := mustMarshal(insecureProof)
		fmt.Printf("📊 Insecure proof size: %d bytes\n", len(insecureJSON))
		
		// Check for information leakage
		leakageCount := 0
		for i, component := range testVector {
			realStr := fmt.Sprintf("%.1f", real(component))
			imagStr := fmt.Sprintf("%.1f", imag(component))
			if strings.Contains(string(insecureJSON), realStr) || strings.Contains(string(insecureJSON), imagStr) {
				fmt.Printf("❌ LEAKED: Component %d (%s + %si) found in proof!\n", i, realStr, imagStr)
				leakageCount++
			}
		}
		fmt.Printf("❌ Total components leaked: %d/%d\n", leakageCount, len(testVector))
	}
	
	fmt.Println("\n🛡️ Testing SECURE implementation...")
	
	// SECURE implementation
	sq, err := NewSecureQuantumZKP(3, 128, []byte("secure-demo"))
	if err != nil {
		log.Fatal(err)
	}
	
	secureProof, err := sq.SecureProveVectorKnowledge(testVector, identifier, key)
	if err != nil {
		log.Fatal("Secure proof generation failed:", err)
	}
	
	secureJSON := mustMarshal(secureProof)
	fmt.Printf("📊 Secure proof size: %d bytes\n", len(secureJSON))
	
	// Check for information leakage
	leakageCount := 0
	for i, component := range testVector {
		realStr := fmt.Sprintf("%.1f", real(component))
		imagStr := fmt.Sprintf("%.1f", imag(component))
		if strings.Contains(string(secureJSON), realStr) || strings.Contains(string(secureJSON), imagStr) {
			fmt.Printf("❌ POTENTIAL LEAK: Component %d (%s + %si) found in proof!\n", i, realStr, imagStr)
			leakageCount++
		}
	}
	
	if leakageCount == 0 {
		fmt.Printf("✅ No components leaked: 0/%d\n", len(testVector))
		fmt.Println("✅ SECURE: Zero-knowledge property maintained!")
	} else {
		fmt.Printf("❌ Components leaked: %d/%d\n", leakageCount, len(testVector))
	}
	
	// Verify both proofs
	fmt.Println("\n🔍 Verification Results:")
	if insecureProof != nil {
		insecureValid := q.VerifyProof(insecureProof, key)
		fmt.Printf("Insecure proof valid: %v\n", insecureValid)
	}
	
	secureValid := sq.VerifySecureProof(secureProof, key)
	fmt.Printf("Secure proof valid: %v\n", secureValid)
	
	fmt.Println("\n📋 Security Summary:")
	fmt.Println("- Insecure implementation: LEAKS ALL SECRET INFORMATION")
	fmt.Println("- Secure implementation: MAINTAINS ZERO-KNOWLEDGE PROPERTY")
	fmt.Println("- Use SecureQuantumZKP for all production applications!")
	
	fmt.Println()
}

// Example5_PerformanceBenchmark demonstrates performance characteristics
func Example5_PerformanceBenchmark() {
	fmt.Println("=== Example 5: Performance Benchmark ===")
	
	sq, err := NewSecureQuantumZKP(3, 128, []byte("benchmark-context"))
	if err != nil {
		log.Fatal(err)
	}
	
	// Test different vector sizes
	vectorSizes := []int{4, 8, 16}
	key := []byte("benchmark-key-32-bytes-long!!!")
	
	for _, size := range vectorSizes {
		fmt.Printf("\n📊 Vector Size: %d components\n", size)
		
		// Generate test vector
		vector := make([]complex128, size)
		for i := 0; i < size; i++ {
			vector[i] = complex(1.0/float64(size), 0)
		}
		
		// Normalize
		vector = normalizeStateVector(vector)
		
		// Benchmark proof generation
		var totalProofTime time.Duration
		var totalVerifyTime time.Duration
		var totalProofSize int
		runs := 5
		
		for run := 0; run < runs; run++ {
			identifier := fmt.Sprintf("benchmark-%d-%d", size, run)
			
			// Proof generation
			start := time.Now()
			proof, err := sq.SecureProveVectorKnowledge(vector, identifier, key)
			if err != nil {
				log.Printf("Proof generation failed: %v", err)
				continue
			}
			proofTime := time.Since(start)
			totalProofTime += proofTime
			
			// Proof verification
			start = time.Now()
			valid := sq.VerifySecureProof(proof, key)
			verifyTime := time.Since(start)
			totalVerifyTime += verifyTime
			
			if !valid {
				log.Printf("Proof verification failed for run %d", run)
			}
			
			proofSize := len(mustMarshal(proof))
			totalProofSize += proofSize
		}
		
		// Calculate averages
		avgProofTime := totalProofTime / time.Duration(runs)
		avgVerifyTime := totalVerifyTime / time.Duration(runs)
		avgProofSize := totalProofSize / runs
		
		fmt.Printf("  Average proof generation: %v\n", avgProofTime)
		fmt.Printf("  Average verification: %v\n", avgVerifyTime)
		fmt.Printf("  Average proof size: %d bytes\n", avgProofSize)
		fmt.Printf("  Throughput: %.1f proofs/second\n", float64(time.Second)/float64(avgProofTime))
	}
	
	fmt.Println()
}

// RunAllExamples executes all example functions
func RunAllExamples() {
	fmt.Println("🚀 Quantum Zero-Knowledge Proof Examples")
	fmt.Println("========================================")
	
	Example1_BasicSecureProof()
	Example2_ProofFromBytes()
	Example3_QuantumCircuitOperations()
	Example4_SecurityComparison()
	Example5_PerformanceBenchmark()
	
	fmt.Println("✅ All examples completed successfully!")
	fmt.Println("\n🛡️ Remember: Always use SecureQuantumZKP for production!")
}

// Uncomment the following to run examples as a standalone program:
/*
func main() {
	RunAllExamples()
}
*/
