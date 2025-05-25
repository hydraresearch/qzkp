package main

import (
    "fmt"
    "math"
    "os"
    "testing"
)

func TestIBMQuantumIntegration(t *testing.T) {
    // Skip if no API key is provided
    if os.Getenv("IQKAPI") == "" {
        t.Skip("Skipping IBM Quantum test: No API key provided")
    }

    // Create IBM Quantum client
    ibm, err := NewIBMQuantumClient()
    if err != nil {
        t.Fatalf("Failed to create IBM Quantum client: %v", err)
    }

    // Test authentication
    err = ibm.Authenticate()
    if err != nil {
        t.Fatalf("Authentication failed: %v", err)
    }

    t.Log("Successfully authenticated with IBM Quantum")

    // Get available backends
    backends, err := ibm.GetAvailableBackends()
    if err != nil {
        t.Fatalf("Failed to get backends: %v", err)
    }

    t.Logf("Available backends: %v", backends)

    // Generate and cache real quantum states
    t.Log("🚀 Generating real quantum states from IBM Quantum...")
    library, err := ibm.GenerateRealQuantumStates()
    if err != nil {
        t.Fatalf("Failed to generate real quantum states: %v", err)
    }

    t.Logf("Generated %d real quantum states", len(library.States))

    // Test ZKP with real quantum states
    ctx := []byte("ibm-quantum-test")
    sq, err := NewSecureQuantumZKP(3, 128, ctx)
    if err != nil {
        t.Fatalf("Failed to create SecureQuantumZKP: %v", err)
    }

    // Test each real quantum state
    for i, realState := range library.States {
        t.Logf("Testing real state %d: %s (%s)", i, realState.Name, realState.Description)
        t.Logf("  Backend: %s, Fidelity: %.3f, Coherence: %.3f",
               realState.Backend, realState.Fidelity, realState.Coherence)

        // Generate proof using real quantum state
        identifier := fmt.Sprintf("real-ibm-state-%s", realState.Name)
        key := []byte("ibm-quantum-test-key-32-bytes!!!!!")

        proof, err := sq.SecureProveVectorKnowledge(realState.Vector, identifier, key)
        if err != nil {
            t.Fatalf("Failed to generate proof for real state %s: %v", realState.Name, err)
        }

        // Verify proof
        valid := sq.VerifySecureProof(proof, key)
        if !valid {
            t.Errorf("Proof verification failed for real state %s", realState.Name)
        } else {
            t.Logf("✅ Proof verification succeeded for real state %s", realState.Name)
        }
    }

    // Test cache functionality
    t.Log("🔄 Testing quantum state cache...")
    cachedStates, err := GetRealQuantumStates(3, 2) // Get 3 states with 2 qubits
    if err != nil {
        t.Fatalf("Failed to get cached quantum states: %v", err)
    }

    t.Logf("Retrieved %d cached quantum states with 2 qubits", len(cachedStates))

    // Test with cached states
    for i, state := range cachedStates {
        if i >= 2 { // Limit to first 2 for testing
            break
        }

        t.Logf("Testing cached state %d: %v", i, formatStateVector(state))

        identifier := fmt.Sprintf("cached-state-%d", i)
        key := []byte("cached-test-key-32-bytes!!!!!!!!")

        proof, err := sq.SecureProveVectorKnowledge(state, identifier, key)
        if err != nil {
            t.Fatalf("Failed to generate proof for cached state %d: %v", i, err)
        }

        valid := sq.VerifySecureProof(proof, key)
        if !valid {
            t.Errorf("Proof verification failed for cached state %d", i)
        } else {
            t.Logf("✅ Cached state %d proof verification succeeded", i)
        }
    }
}

// formatStateVector formats a state vector for display
func formatStateVector(state []complex128) string {
    if len(state) > 8 {
        // Truncate for display
        return fmt.Sprintf("[%v, %v, %v, ..., %v]",
            state[0], state[1], state[2], state[len(state)-1])
    }
    return fmt.Sprintf("%v", state)
}

// TestQuantumSafe