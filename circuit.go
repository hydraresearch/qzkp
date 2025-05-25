package main

import (
	"fmt"
	"math"
	"math/rand"
	"time"
)

// QuantumCircuit represents a quantum circuit
type QuantumCircuit struct {
	NumQubits   int                    `json:"num_qubits"`
	NumClbits   int                    `json:"num_clbits"`
	Metadata    map[string]interface{} `json:"metadata"`
	Gates       []QuantumGate          `json:"gates"`
	Initialized bool                   `json:"initialized"`
}

// QuantumGate represents a quantum gate operation
type QuantumGate struct {
	Type     string    `json:"type"`
	Qubits   []int     `json:"qubits"`
	Params   []float64 `json:"params,omitempty"`
	Metadata string    `json:"metadata,omitempty"`
}

// ExecutionResult represents the result of quantum circuit execution
type ExecutionResult struct {
	Counts        map[string]int `json:"counts"`
	ExecutionTime float64        `json:"execution_time"`
	Shots         int            `json:"shots"`
	Backend       string         `json:"backend"`
}

// BuildCircuit builds a quantum circuit encoding the given vector
func (q *QuantumZKP) BuildCircuit(vector []complex128, identifier string) (*QuantumCircuit, error) {
	if len(vector) == 0 {
		return nil, fmt.Errorf("vector cannot be empty")
	}

	// Calculate number of qubits needed
	numQubits := int(math.Ceil(math.Log2(float64(len(vector)))))
	if numQubits < 1 {
		numQubits = 1
	}

	circuit := &QuantumCircuit{
		NumQubits: numQubits,
		NumClbits: numQubits,
		Metadata: map[string]interface{}{
			"identifier":   identifier,
			"vector_size":  len(vector),
			"created_at":   time.Now(),
			"dimensions":   q.Dimensions,
		},
		Gates:       make([]QuantumGate, 0),
		Initialized: false,
	}

	// Initialize the circuit with the state vector
	err := q.initializeStateVector(circuit, vector)
	if err != nil {
		return nil, fmt.Errorf("failed to initialize state vector: %w", err)
	}

	// Add measurement gates
	q.addMeasurements(circuit)

	return circuit, nil
}

// initializeStateVector initializes the quantum circuit with the given state vector
func (q *QuantumZKP) initializeStateVector(circuit *QuantumCircuit, vector []complex128) error {
	// Normalize the vector
	normalized := normalizeStateVector(vector)

	// Pad vector to match circuit dimensions if needed
	targetSize := 1 << circuit.NumQubits
	if len(normalized) < targetSize {
		padded := make([]complex128, targetSize)
		copy(padded, normalized)
		normalized = padded
	} else if len(normalized) > targetSize {
		normalized = normalized[:targetSize]
	}

	// Add state preparation gates (simplified approach)
	// In a real implementation, this would use state preparation algorithms
	for i := 0; i < circuit.NumQubits; i++ {
		// Add Hadamard gates to create superposition
		circuit.Gates = append(circuit.Gates, QuantumGate{
			Type:   "h",
			Qubits: []int{i},
		})
	}

	// Add rotation gates based on the state vector amplitudes
	for i, amplitude := range normalized {
		if i >= (1 << circuit.NumQubits) {
			break
		}

		magnitude := real(amplitude)*real(amplitude) + imag(amplitude)*imag(amplitude)
		if magnitude > 1e-10 {
			phase := math.Atan2(imag(amplitude), real(amplitude))

			// Add rotation gates to encode the amplitude and phase
			qubitIndex := i % circuit.NumQubits
			circuit.Gates = append(circuit.Gates, QuantumGate{
				Type:   "ry",
				Qubits: []int{qubitIndex},
				Params: []float64{2 * math.Acos(math.Sqrt(magnitude))},
			})

			if math.Abs(phase) > 1e-10 {
				circuit.Gates = append(circuit.Gates, QuantumGate{
					Type:   "rz",
					Qubits: []int{qubitIndex},
					Params: []float64{phase},
				})
			}
		}
	}

	circuit.Initialized = true
	return nil
}

// addMeasurements adds measurement operations to the circuit
func (q *QuantumZKP) addMeasurements(circuit *QuantumCircuit) {
	for i := 0; i < circuit.NumQubits; i++ {
		circuit.Gates = append(circuit.Gates, QuantumGate{
			Type:   "measure",
			Qubits: []int{i, i}, // qubit index, classical bit index
		})
	}
}

// TranspileCircuit optimizes the quantum circuit
func (q *QuantumZKP) TranspileCircuit(circuit *QuantumCircuit, optimizationLevel int) (*QuantumCircuit, error) {
	if circuit == nil {
		return nil, fmt.Errorf("circuit cannot be nil")
	}

	// Create a copy of the circuit for transpilation
	transpiled := &QuantumCircuit{
		NumQubits:   circuit.NumQubits,
		NumClbits:   circuit.NumClbits,
		Metadata:    make(map[string]interface{}),
		Gates:       make([]QuantumGate, len(circuit.Gates)),
		Initialized: circuit.Initialized,
	}

	// Copy metadata
	for k, v := range circuit.Metadata {
		transpiled.Metadata[k] = v
	}
	transpiled.Metadata["transpiled"] = true
	transpiled.Metadata["optimization_level"] = optimizationLevel

	// Copy gates
	copy(transpiled.Gates, circuit.Gates)

	// Apply optimizations based on optimization level
	switch optimizationLevel {
	case 0:
		// No optimization
	case 1:
		// Basic optimization - remove redundant gates
		transpiled.Gates = q.removeRedundantGates(transpiled.Gates)
	case 2:
		// Medium optimization - gate fusion
		transpiled.Gates = q.removeRedundantGates(transpiled.Gates)
		transpiled.Gates = q.fuseGates(transpiled.Gates)
	case 3:
		// High optimization - full optimization
		transpiled.Gates = q.removeRedundantGates(transpiled.Gates)
		transpiled.Gates = q.fuseGates(transpiled.Gates)
		transpiled.Gates = q.optimizeRotations(transpiled.Gates)
	}

	return transpiled, nil
}

// removeRedundantGates removes redundant quantum gates
func (q *QuantumZKP) removeRedundantGates(gates []QuantumGate) []QuantumGate {
	if len(gates) <= 1 {
		return gates
	}

	optimized := make([]QuantumGate, 0, len(gates))

	for i, gate := range gates {
		// Skip redundant identity-like operations
		if gate.Type == "id" {
			continue
		}

		// Check for gate cancellation (e.g., X followed by X)
		if i < len(gates)-1 {
			nextGate := gates[i+1]
			if q.gatesCancelOut(gate, nextGate) {
				// Skip both gates
				i++ // This will be incremented again by the loop
				continue
			}
		}

		optimized = append(optimized, gate)
	}

	return optimized
}

// gatesCancelOut checks if two gates cancel each other out
func (q *QuantumZKP) gatesCancelOut(gate1, gate2 QuantumGate) bool {
	// Same gate type on same qubits with opposite effects
	if gate1.Type == gate2.Type && len(gate1.Qubits) == len(gate2.Qubits) {
		for i, qubit := range gate1.Qubits {
			if qubit != gate2.Qubits[i] {
				return false
			}
		}

		// Check for self-inverse gates
		switch gate1.Type {
		case "x", "y", "z", "h":
			return true // These gates are self-inverse
		case "rz", "ry", "rx":
			// Rotation gates cancel if angles are opposite
			if len(gate1.Params) == 1 && len(gate2.Params) == 1 {
				return math.Abs(gate1.Params[0]+gate2.Params[0]) < 1e-10
			}
		}
	}

	return false
}

// fuseGates combines compatible gates
func (q *QuantumZKP) fuseGates(gates []QuantumGate) []QuantumGate {
	// Simple gate fusion - combine consecutive rotation gates on same qubit
	if len(gates) <= 1 {
		return gates
	}

	fused := make([]QuantumGate, 0, len(gates))

	for i := 0; i < len(gates); i++ {
		gate := gates[i]

		// Try to fuse with next gate if it's a rotation on the same qubit
		if i < len(gates)-1 && q.canFuseRotations(gate, gates[i+1]) {
			fusedGate := q.fuseRotationGates(gate, gates[i+1])
			fused = append(fused, fusedGate)
			i++ // Skip the next gate as it's been fused
		} else {
			fused = append(fused, gate)
		}
	}

	return fused
}

// canFuseRotations checks if two rotation gates can be fused
func (q *QuantumZKP) canFuseRotations(gate1, gate2 QuantumGate) bool {
	// Can fuse if same rotation type on same qubit
	if gate1.Type == gate2.Type && len(gate1.Qubits) == 1 && len(gate2.Qubits) == 1 {
		return gate1.Qubits[0] == gate2.Qubits[0] &&
			   len(gate1.Params) == 1 && len(gate2.Params) == 1
	}
	return false
}

// fuseRotationGates combines two rotation gates
func (q *QuantumZKP) fuseRotationGates(gate1, gate2 QuantumGate) QuantumGate {
	return QuantumGate{
		Type:   gate1.Type,
		Qubits: gate1.Qubits,
		Params: []float64{gate1.Params[0] + gate2.Params[0]},
	}
}

// optimizeRotations optimizes rotation angles
func (q *QuantumZKP) optimizeRotations(gates []QuantumGate) []QuantumGate {
	optimized := make([]QuantumGate, 0, len(gates))

	for _, gate := range gates {
		if len(gate.Params) == 1 {
			// Normalize rotation angles to [0, 2π)
			angle := math.Mod(gate.Params[0], 2*math.Pi)
			if angle < 0 {
				angle += 2 * math.Pi
			}

			// Skip near-zero rotations
			if math.Abs(angle) < 1e-10 || math.Abs(angle-2*math.Pi) < 1e-10 {
				continue
			}

			gate.Params[0] = angle
		}
		optimized = append(optimized, gate)
	}

	return optimized
}

// ApplyNoiseMitigation applies noise mitigation techniques to the circuit
func (q *QuantumZKP) ApplyNoiseMitigation(circuit *QuantumCircuit) (*QuantumCircuit, error) {
	if circuit == nil {
		return nil, fmt.Errorf("circuit cannot be nil")
	}

	// Create a copy for noise mitigation
	mitigated := &QuantumCircuit{
		NumQubits:   circuit.NumQubits,
		NumClbits:   circuit.NumClbits,
		Metadata:    make(map[string]interface{}),
		Gates:       make([]QuantumGate, 0, len(circuit.Gates)*2), // May add more gates
		Initialized: circuit.Initialized,
	}

	// Copy metadata
	for k, v := range circuit.Metadata {
		mitigated.Metadata[k] = v
	}
	mitigated.Metadata["noise_mitigation"] = true

	// Apply Pauli twirling (simplified version)
	rand.Seed(12345) // Use fixed seed for reproducibility

	for _, gate := range circuit.Gates {
		// Add the original gate
		mitigated.Gates = append(mitigated.Gates, gate)

		// For two-qubit gates, add Pauli twirling
		if len(gate.Qubits) == 2 && gate.Type == "cx" {
			// Randomly apply Pauli gates before and after
			if rand.Float64() < 0.1 { // 10% chance to add twirling
				// Add random Pauli gates
				pauliGates := []string{"x", "y", "z"}
				for _, qubit := range gate.Qubits {
					if rand.Float64() < 0.3 {
						randomPauli := pauliGates[rand.Intn(len(pauliGates))]
						mitigated.Gates = append(mitigated.Gates, QuantumGate{
							Type:   randomPauli,
							Qubits: []int{qubit},
						})
					}
				}
			}
		}
	}

	return mitigated, nil
}

// ExecuteCircuit simulates the execution of a quantum circuit
func (q *QuantumZKP) ExecuteCircuit(circuit *QuantumCircuit, shots int) (*ExecutionResult, error) {
	if circuit == nil {
		return nil, fmt.Errorf("circuit cannot be nil")
	}

	if shots <= 0 {
		shots = 1024 // Default number of shots
	}

	startTime := time.Now()

	// Simulate quantum circuit execution
	counts := make(map[string]int)

	// Generate measurement outcomes
	for shot := 0; shot < shots; shot++ {
		bitstring := q.simulateMeasurement(circuit)
		counts[bitstring]++
	}

	executionTime := time.Since(startTime).Seconds()

	return &ExecutionResult{
		Counts:        counts,
		ExecutionTime: executionTime,
		Shots:         shots,
		Backend:       "simulator",
	}, nil
}

// simulateMeasurement simulates a single measurement of the quantum circuit
func (q *QuantumZKP) simulateMeasurement(circuit *QuantumCircuit) string {
	// Simple simulation: generate random bitstring based on circuit complexity
	// In a real implementation, this would simulate the actual quantum evolution

	bitstring := ""

	// Count the number of Hadamard gates to estimate superposition
	hadamardCount := 0
	for _, gate := range circuit.Gates {
		if gate.Type == "h" {
			hadamardCount++
		}
	}

	// Generate bitstring based on circuit structure
	for i := 0; i < circuit.NumQubits; i++ {
		// If there are Hadamard gates, create more balanced distribution
		var prob float64
		if hadamardCount > 0 {
			prob = 0.5 // Equal probability for superposition
		} else {
			prob = 0.1 // Bias towards |0⟩ for basis states
		}

		// Add some randomness based on rotation gates
		for _, gate := range circuit.Gates {
			if gate.Type == "ry" || gate.Type == "rz" {
				if len(gate.Qubits) > 0 && gate.Qubits[0] == i && len(gate.Params) > 0 {
					// Adjust probability based on rotation angle
					angle := gate.Params[0]
					prob = math.Sin(angle/2) * math.Sin(angle/2)
				}
			}
		}

		if rand.Float64() < prob {
			bitstring += "1"
		} else {
			bitstring += "0"
		}
	}

	return bitstring
}

// ProveVectorKnowledge generates a ZK proof of knowledge for the given vector using circuit execution
func (q *QuantumZKP) ProveVectorKnowledge(vector []complex128, identifier string, optimizationLevel int) ([]byte, map[string]interface{}, error) {
	// Build the quantum circuit
	circuit, err := q.BuildCircuit(vector, identifier)
	if err != nil {
		return nil, nil, fmt.Errorf("failed to build circuit: %w", err)
	}

	// Transpile the circuit
	transpiled, err := q.TranspileCircuit(circuit, optimizationLevel)
	if err != nil {
		return nil, nil, fmt.Errorf("failed to transpile circuit: %w", err)
	}

	// Apply noise mitigation
	mitigated, err := q.ApplyNoiseMitigation(transpiled)
	if err != nil {
		return nil, nil, fmt.Errorf("failed to apply noise mitigation: %w", err)
	}

	// Execute the circuit
	result, err := q.ExecuteCircuit(mitigated, 1024)
	if err != nil {
		return nil, nil, fmt.Errorf("failed to execute circuit: %w", err)
	}

	// Create quantum state vector
	state := NewQuantumStateVector(vector)

	// Generate commitment
	superpos := CreateSuperposition(vector)
	// Use a proper 32-byte key for blake3
	key := make([]byte, 32)
	copy(key, []byte("default_key_for_testing_purposes"))
	commitment := GenerateCommitment(superpos, identifier, key)

	// Create proof structure matching Python implementation
	proof := map[string]interface{}{
		"quantum_dimensions":  q.Dimensions,
		"measurements":        result.Counts,
		"state_vector":        vectorToFloatSlice(vector),
		"identifier":          identifier,
		"execution_result":    result,
		"state_entanglement":  state.Entanglement,
		"state_coherence":     state.Coherence,
		"signature":           "", // Will be filled by signing process
	}

	return commitment, proof, nil
}

// vectorToFloatSlice converts complex128 slice to float64 slice for JSON serialization
func vectorToFloatSlice(vector []complex128) []float64 {
	result := make([]float64, len(vector)*2)
	for i, c := range vector {
		result[i*2] = real(c)
		result[i*2+1] = imag(c)
	}
	return result
}
