package main

import (
	"encoding/json"
	"math"
	"time"
)

// NewQuantumStateVector creates a new quantum state vector from coordinates
func NewQuantumStateVector(coordinates []complex128) *QuantumStateVector {
	if len(coordinates) == 0 {
		panic("State vector must not be empty")
	}

	// Normalize the coordinates
	normalized := normalizeStateVector(coordinates)

	// Calculate phase
	phase := make([]float64, len(normalized))
	for i, c := range normalized {
		phase[i] = math.Atan2(imag(c), real(c))
	}

	// Calculate entanglement and coherence
	entanglement := calculateEntanglement(normalized)
	coherence := calculateCoherence(normalized)

	return &QuantumStateVector{
		Coordinates:  normalized,
		Phase:        phase,
		Entanglement: entanglement,
		Coherence:    coherence,
		StateType:    "SUPERPOSITION",
		Timestamp:    time.Now(),
	}
}

func (qsv *QuantumStateVector) Serialize() ([]byte, error) {
	return json.Marshal(qsv)
}
