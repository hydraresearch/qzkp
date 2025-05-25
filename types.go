package main

import "time"

type QuantumStateVector struct {
	Coordinates  []complex128 `json:"coordinates"`
	Phase        []float64    `json:"phase"`
	Entanglement float64      `json:"entanglement"`
	Coherence    float64      `json:"coherence"`
	StateType    string       `json:"state_type"`
	Timestamp    time.Time    `json:"timestamp"`
}



type Superposition struct {
	States     []complex128
	Amplitudes []float64
}

// Proof matches your Python‐style proof JSON.
type Proof struct {
	QuantumDimensions int           `json:"quantum_dimensions"`
	BasisCoefficients [][]float64   `json:"basis_coefficients"`
	Amplitudes        []float64     `json:"amplitudes"`
	Measurements      []Measurement `json:"measurements"`
	StateMetadata     StateMetadata `json:"state_metadata"`
	Identifier        string        `json:"identifier"`
	Signature         string        `json:"signature"`
	Commitment        string        `json:"commitment"`
}

type Measurement struct {
	BasisIndex       int     `json:"basis_index"`
	Probability      float64 `json:"probability"`
	Phase            float64 `json:"phase"`
	MeasurementBasis string  `json:"measurement_basis"`
}

type StateMetadata struct {
	Coherence    float64   `json:"coherence"`
	Entanglement float64   `json:"entanglement"`
	Timestamp    time.Time `json:"timestamp"`
}
