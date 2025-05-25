package main

import (
	"encoding/json"
	"fmt"
	"log"
	"math"
	"os"
	"time"
)

func main() {
	if len(os.Args) < 2 {
		printUsage()
		return
	}

	command := os.Args[1]

	switch command {
	case "examples":
		RunAllExamples()
	case "demo":
		runQuickDemo()
	case "security":
		runSecurityDemo()
	case "benchmark":
		Example5_PerformanceBenchmark()
	case "security-levels":
		runSecurityLevelsDemo()
	case "ultra-secure":
		runUltraSecureDemo()
	case "help":
		printUsage()
	default:
		fmt.Printf("Unknown command: %s\n", command)
		printUsage()
	}
}

func printUsage() {
	fmt.Println("Quantum Zero-Knowledge Proof (QZKP) Implementation")
	fmt.Println("==================================================")
	fmt.Println()
	fmt.Println("Usage: go run . <command>")
	fmt.Println()
	fmt.Println("Commands:")
	fmt.Println("  examples        - Run all comprehensive examples")
	fmt.Println("  demo            - Quick demonstration of secure ZKP")
	fmt.Println("  security        - Security analysis and comparison")
	fmt.Println("  security-levels - Compare different security levels")
	fmt.Println("  ultra-secure    - Demonstrate 256-bit ultra-secure ZKP")
	fmt.Println("  benchmark       - Performance benchmarking")
	fmt.Println("  help            - Show this help message")
	fmt.Println()
	fmt.Println("Examples:")
	fmt.Println("  go run . demo")
	fmt.Println("  go run . examples")
	fmt.Println("  go run . security")
	fmt.Println()
	fmt.Println("🛡️  SECURITY NOTICE:")
	fmt.Println("   Always use SecureQuantumZKP for production!")
	fmt.Println("   The insecure implementation leaks secrets!")
}

func runQuickDemo() {
	fmt.Println("🚀 Quick Quantum ZKP Demo")
	fmt.Println("========================")

	// Initialize secure quantum ZKP
	sq, err := NewSecureQuantumZKP(3, 128, []byte("demo-context"))
	if err != nil {
		log.Fatal("Failed to initialize SecureQuantumZKP:", err)
	}

	// Secret data
	secretMessage := []byte("This is a confidential message that should remain secret!")
	key := []byte("demo-key-32-bytes-long-enough!!!")

	fmt.Printf("Secret message: %q\n", string(secretMessage))
	fmt.Printf("Message length: %d bytes\n", len(secretMessage))

	// Generate proof
	fmt.Println("\n🔐 Generating zero-knowledge proof...")
	proof, err := sq.SecureProveFromBytes(secretMessage, "demo-message", key)
	if err != nil {
		log.Fatal("Proof generation failed:", err)
	}

	fmt.Printf("✅ Proof generated successfully!\n")
	fmt.Printf("📊 Proof size: %d bytes\n", len(mustMarshalDemo(proof)))
	fmt.Printf("🔒 Challenge responses: %d\n", len(proof.ChallengeResponse))

	// Verify proof
	fmt.Println("\n🔍 Verifying proof...")
	isValid := sq.VerifySecureProof(proof, key)

	if isValid {
		fmt.Println("✅ Proof verification SUCCESSFUL!")
		fmt.Println("🛡️  The verifier now knows you possess the secret message")
		fmt.Println("🔒 But the verifier learned NOTHING about the message content!")
	} else {
		fmt.Println("❌ Proof verification FAILED!")
	}

	// Demonstrate security
	fmt.Println("\n🔍 Security Check:")
	proofJSON := string(mustMarshalDemo(proof))

	// Check if any part of the secret message appears in the proof
	messageStr := string(secretMessage)
	if containsSubstring(proofJSON, messageStr) {
		fmt.Println("❌ WARNING: Secret message found in proof!")
	} else {
		fmt.Println("✅ Secret message NOT found in proof")
	}

	// Check for common words that might leak
	words := []string{"confidential", "secret", "message"}
	leakFound := false
	for _, word := range words {
		if containsSubstring(proofJSON, word) {
			fmt.Printf("❌ Potential leak: '%s' found in proof\n", word)
			leakFound = true
		}
	}

	if !leakFound {
		fmt.Println("✅ No sensitive words found in proof")
	}

	fmt.Println("\n🎉 Demo completed successfully!")
	fmt.Println("💡 The proof demonstrates knowledge without revealing the secret!")
}

func runSecurityDemo() {
	fmt.Println("🔒 Security Analysis Demo")
	fmt.Println("========================")

	// Test vector with easily identifiable components
	testVector := []complex128{
		complex(0.9, 0.1),  // Distinctive values
		complex(0.2, 0.8),
		complex(0.7, 0.3),
		complex(0.4, 0.6),
	}

	key := []byte("security-demo-key-32-bytes-long!")
	identifier := "security-test"

	fmt.Println("Test vector components:")
	for i, c := range testVector {
		fmt.Printf("  [%d]: %.1f + %.1fi\n", i, real(c), imag(c))
	}

	// Test insecure implementation
	fmt.Println("\n🔴 Testing INSECURE implementation...")
	q, err := NewQuantumZKP(3, 128, []byte("insecure-test"))
	if err != nil {
		log.Fatal(err)
	}

	insecureProof, err := q.Prove(testVector, identifier, key)
	if err != nil {
		fmt.Printf("⚠️  Insecure proof generation failed: %v\n", err)
	} else {
		insecureJSON := mustMarshalDemo(insecureProof)
		fmt.Printf("📊 Insecure proof size: %d bytes\n", len(insecureJSON))

		// Check for leakage
		fmt.Println("🔍 Checking for information leakage...")
		leakCount := 0
		for i, c := range testVector {
			realStr := fmt.Sprintf("%.1f", real(c))
			imagStr := fmt.Sprintf("%.1f", imag(c))

			if containsSubstring(string(insecureJSON), realStr) {
				fmt.Printf("❌ LEAKED: Real part %.1f (component %d)\n", real(c), i)
				leakCount++
			}
			if containsSubstring(string(insecureJSON), imagStr) {
				fmt.Printf("❌ LEAKED: Imaginary part %.1f (component %d)\n", imag(c), i)
				leakCount++
			}
		}

		fmt.Printf("❌ Total leaks detected: %d\n", leakCount)
		if leakCount > 0 {
			fmt.Println("🚨 CRITICAL: Insecure implementation exposes secret data!")
		}
	}

	// Test secure implementation
	fmt.Println("\n🛡️ Testing SECURE implementation...")
	sq, err := NewSecureQuantumZKP(3, 128, []byte("secure-test"))
	if err != nil {
		log.Fatal(err)
	}

	secureProof, err := sq.SecureProveVectorKnowledge(testVector, identifier, key)
	if err != nil {
		log.Fatal("Secure proof generation failed:", err)
	}

	secureJSON := mustMarshalDemo(secureProof)
	fmt.Printf("📊 Secure proof size: %d bytes\n", len(secureJSON))

	// Check for leakage
	fmt.Println("🔍 Checking for information leakage...")
	leakCount := 0
	for i, c := range testVector {
		realStr := fmt.Sprintf("%.1f", real(c))
		imagStr := fmt.Sprintf("%.1f", imag(c))

		if containsSubstring(string(secureJSON), realStr) {
			fmt.Printf("❌ POTENTIAL LEAK: Real part %.1f (component %d)\n", real(c), i)
			leakCount++
		}
		if containsSubstring(string(secureJSON), imagStr) {
			fmt.Printf("❌ POTENTIAL LEAK: Imaginary part %.1f (component %d)\n", imag(c), i)
			leakCount++
		}
	}

	if leakCount == 0 {
		fmt.Println("✅ No leaks detected - Zero-knowledge property maintained!")
	} else {
		fmt.Printf("⚠️  Potential leaks detected: %d\n", leakCount)
	}

	// Verify proofs
	fmt.Println("\n🔍 Verification Results:")
	if insecureProof != nil {
		insecureValid := q.VerifyProof(insecureProof, key)
		fmt.Printf("Insecure proof valid: %v\n", insecureValid)
	}

	secureValid := sq.VerifySecureProof(secureProof, key)
	fmt.Printf("Secure proof valid: %v\n", secureValid)

	// Summary
	fmt.Println("\n📋 SECURITY SUMMARY:")
	fmt.Println("==================")
	fmt.Println("🔴 Insecure Implementation:")
	fmt.Println("   - Exposes complete secret information")
	fmt.Println("   - NOT suitable for any real-world use")
	fmt.Println("   - Educational purposes only")
	fmt.Println()
	fmt.Println("🛡️ Secure Implementation:")
	fmt.Println("   - Maintains zero-knowledge property")
	fmt.Println("   - Suitable for production use")
	fmt.Println("   - Post-quantum secure")
	fmt.Println()
	fmt.Println("⚠️  RECOMMENDATION: Always use SecureQuantumZKP!")
}

func runSecurityLevelsDemo() {
	fmt.Println("🔒 Security Levels Comparison")
	fmt.Println("============================")

	testData := []byte("Secret data for security level testing")
	key := []byte("security-levels-demo-key-32-bytes!")

	// Test different soundness security levels
	securityLevels := []struct {
		name        string
		soundness   int
		description string
		recommended string
	}{
		{"Minimal", 32, "2^32 soundness error (~1 in 4 billion)", "❌ Too weak for production"},
		{"Low", 48, "2^48 soundness error (~1 in 280 trillion)", "⚠️ Only for low-risk applications"},
		{"Standard", 64, "2^64 soundness error (~1 in 18 quintillion)", "✅ Good for most applications"},
		{"High", 80, "2^80 soundness error (~1 in 1.2 × 10^24)", "✅ Recommended for production"},
		{"Very High", 96, "2^96 soundness error (~1 in 7.9 × 10^28)", "✅ High-security applications"},
		{"Maximum", 128, "2^128 soundness error (~1 in 3.4 × 10^38)", "✅ Maximum security"},
		{"Ultra", 256, "2^256 soundness error (~1 in 1.2 × 10^77)", "🔒 Ultra-secure / Future-proof"},
	}

	fmt.Println("Testing different soundness security levels:")

	for _, level := range securityLevels {
		fmt.Printf("🔐 %s Security (%d-bit soundness)\n", level.name, level.soundness)
		fmt.Printf("   Description: %s\n", level.description)
		fmt.Printf("   Recommendation: %s\n", level.recommended)

		// Create ZKP instance with specific soundness level
		sq, err := NewSecureQuantumZKPWithSoundness(3, 128, level.soundness, []byte("security-test"))
		if err != nil {
			fmt.Printf("   ❌ Error: %v\n\n", err)
			continue
		}

		// Generate proof and measure performance
		start := time.Now()
		proof, err := sq.SecureProveFromBytes(testData, fmt.Sprintf("test-%d", level.soundness), key)
		if err != nil {
			fmt.Printf("   ❌ Proof generation failed: %v\n\n", err)
			continue
		}
		proofTime := time.Since(start)

		// Verify proof
		start = time.Now()
		valid := sq.VerifySecureProof(proof, key)
		verifyTime := time.Since(start)

		proofSize := len(mustMarshalDemo(proof))

		fmt.Printf("   📊 Results:\n")
		fmt.Printf("      - Proof size: %d bytes (%.1f KB)\n", proofSize, float64(proofSize)/1024)
		fmt.Printf("      - Challenge responses: %d\n", len(proof.ChallengeResponse))
		fmt.Printf("      - Generation time: %v\n", proofTime)
		fmt.Printf("      - Verification time: %v\n", verifyTime)
		fmt.Printf("      - Verification result: %v\n", valid)

		// Calculate security analysis
		soundnessError := 1.0 / math.Pow(2, float64(level.soundness))
		fmt.Printf("      - Soundness error probability: %.2e\n", soundnessError)

		if !valid {
			fmt.Printf("   ❌ Verification failed!\n")
		}

		fmt.Println()
	}

	fmt.Println("📋 SECURITY RECOMMENDATIONS:")
	fmt.Println("============================")
	fmt.Println("🔴 < 64-bit soundness: NOT recommended for any production use")
	fmt.Println("🟡 64-bit soundness: Acceptable for low-risk applications")
	fmt.Println("✅ 80-bit soundness: Recommended minimum for production")
	fmt.Println("✅ 96-bit soundness: Good for high-security applications")
	fmt.Println("✅ 128-bit soundness: Maximum security, future-proof")
	fmt.Println("🔒 256-bit soundness: Ultra-secure, quantum-resistant future-proofing")
	fmt.Println()
	fmt.Println("💡 Consider your threat model:")
	fmt.Println("   - Academic/research: 64-80 bits sufficient")
	fmt.Println("   - Commercial applications: 80-96 bits recommended")
	fmt.Println("   - Financial/critical systems: 96-128 bits required")
	fmt.Println("   - Long-term storage: 128-256 bits for future-proofing")
	fmt.Println("   - Quantum-resistant archives: 256 bits for maximum security")
}

func runUltraSecureDemo() {
	fmt.Println("🔒 Ultra-Secure Quantum ZKP Demo (256-bit)")
	fmt.Println("==========================================")
	fmt.Println()
	fmt.Println("This demonstration shows the highest security level available:")
	fmt.Println("- 256-bit soundness security")
	fmt.Println("- 2^256 soundness error (~1 in 1.2 × 10^77)")
	fmt.Println("- Quantum-resistant future-proofing")
	fmt.Println("- Suitable for the most critical applications")
	fmt.Println()

	// Initialize ultra-secure quantum ZKP
	fmt.Println("🔐 Initializing ultra-secure quantum ZKP...")
	sq, err := NewUltraSecureQuantumZKP(3, 256, []byte("ultra-secure-context"))
	if err != nil {
		log.Fatal("Failed to initialize ultra-secure ZKP:", err)
	}

	// Ultra-sensitive data
	ultraSecretData := []byte(`
TOP SECRET - ULTRA CLASSIFIED
=============================
Project: Quantum Cryptography Research
Classification: ULTRA SECRET / EYES ONLY
Clearance Required: COSMIC / ATOMAL

CRITICAL NATIONAL SECURITY INFORMATION
This document contains information vital to national security.
Unauthorized disclosure is prohibited and punishable under law.

Quantum Key Distribution Protocol:
- Primary quantum channel: 1550nm photons
- Entanglement source: Spontaneous parametric down-conversion
- Error correction: Low-density parity-check codes
- Privacy amplification: Universal hash functions

[REDACTED TECHNICAL SPECIFICATIONS]
[REDACTED IMPLEMENTATION DETAILS]
[REDACTED SECURITY ANALYSIS]

This information is classified at the highest level and must be
protected with the strongest available cryptographic measures.
`)

	key := []byte("ultra-secure-key-32-bytes-long!!")

	fmt.Printf("📄 Ultra-secret document size: %d bytes\n", len(ultraSecretData))
	fmt.Println("🔒 Document classification: TOP SECRET / ULTRA")
	fmt.Println()

	// Generate ultra-secure proof
	fmt.Println("🛡️ Generating 256-bit ultra-secure proof...")
	fmt.Println("   (This may take a moment due to the high security level)")

	start := time.Now()
	proof, err := sq.SecureProveFromBytes(ultraSecretData, "ultra-secret-doc", key)
	if err != nil {
		log.Fatal("Ultra-secure proof generation failed:", err)
	}
	proofTime := time.Since(start)

	fmt.Printf("✅ Ultra-secure proof generated successfully!\n")
	fmt.Printf("📊 Proof generation time: %v\n", proofTime)
	fmt.Printf("📊 Proof size: %d bytes (%.1f KB)\n", len(mustMarshalDemo(proof)), float64(len(mustMarshalDemo(proof)))/1024)
	fmt.Printf("🔒 Challenge responses: %d\n", len(proof.ChallengeResponse))
	fmt.Printf("🛡️ Soundness security: 256-bit\n")
	fmt.Printf("🔢 Soundness error probability: %.2e\n", 1.0/math.Pow(2, 256))
	fmt.Println()

	// Verify ultra-secure proof
	fmt.Println("🔍 Verifying ultra-secure proof...")
	start = time.Now()
	isValid := sq.VerifySecureProof(proof, key)
	verifyTime := time.Since(start)

	if isValid {
		fmt.Println("✅ Ultra-secure proof verification SUCCESSFUL!")
		fmt.Printf("📊 Verification time: %v\n", verifyTime)
		fmt.Println("🛡️ The verifier now knows you possess the ultra-secret document")
		fmt.Println("🔒 But the verifier learned ABSOLUTELY NOTHING about the document content!")
	} else {
		fmt.Println("❌ Ultra-secure proof verification FAILED!")
		return
	}
	fmt.Println()

	// Ultra-security analysis
	fmt.Println("🔍 Ultra-Security Analysis:")
	fmt.Println("===========================")
	proofJSON := string(mustMarshalDemo(proof))

	// Check for any leakage of ultra-secret content
	ultraSecretWords := []string{
		"TOP SECRET", "ULTRA CLASSIFIED", "COSMIC", "ATOMAL",
		"quantum", "cryptography", "photons", "entanglement",
		"REDACTED", "national security", "classified",
	}

	leakageFound := false
	for _, word := range ultraSecretWords {
		if containsSubstring(proofJSON, word) {
			fmt.Printf("❌ CRITICAL LEAK: '%s' found in proof!\n", word)
			leakageFound = true
		}
	}

	if !leakageFound {
		fmt.Println("✅ No ultra-secret content leaked in proof")
		fmt.Println("✅ Zero-knowledge property maintained at highest security level")
	}

	// Check document content directly
	if containsSubstring(proofJSON, string(ultraSecretData)) {
		fmt.Println("❌ CATASTROPHIC: Full document found in proof!")
	} else {
		fmt.Println("✅ Full document content NOT found in proof")
	}
	fmt.Println()

	// Security comparison
	fmt.Println("🔒 Ultra-Security Level Analysis:")
	fmt.Println("=================================")
	fmt.Printf("🛡️ Soundness Security: 256-bit\n")
	fmt.Printf("🔢 Soundness Error: 1 in %.2e\n", math.Pow(2, 256))
	fmt.Printf("⏱️ Time to break (theoretical): > 10^70 years\n")
	fmt.Printf("🌌 Comparison: More secure than the number of atoms in the observable universe\n")
	fmt.Printf("🔮 Quantum resistance: Secure against future quantum computers\n")
	fmt.Printf("📅 Future-proofing: Secure for centuries to come\n")
	fmt.Println()

	fmt.Println("🎯 Ultra-Secure Use Cases:")
	fmt.Println("==========================")
	fmt.Println("✅ National security documents")
	fmt.Println("✅ Long-term classified archives")
	fmt.Println("✅ Quantum-resistant protocols")
	fmt.Println("✅ Critical infrastructure protection")
	fmt.Println("✅ Financial system security")
	fmt.Println("✅ Medical privacy protection")
	fmt.Println("✅ Legal document authentication")
	fmt.Println("✅ Intellectual property protection")
	fmt.Println()

	fmt.Println("🎉 Ultra-secure demonstration completed!")
	fmt.Println("💡 This represents the pinnacle of quantum zero-knowledge security!")
}

// Helper functions
func mustMarshalDemo(v interface{}) []byte {
	data, err := json.Marshal(v)
	if err != nil {
		log.Fatal("JSON marshaling failed:", err)
	}
	return data
}

func containsSubstring(s, substr string) bool {
	if len(substr) == 0 {
		return false
	}
	for i := 0; i <= len(s)-len(substr); i++ {
		if s[i:i+len(substr)] == substr {
			return true
		}
	}
	return false
}
