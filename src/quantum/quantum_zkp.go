package main

import (
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"time"
)

// QuantumZKP holds configuration and signer
type QuantumZKP struct {
	Dimensions    int
	SecurityLevel int
	Cache         *ResultCache
	Signer        *SignatureScheme
}

// NewQuantumZKP constructs a new instance with given dimensions and security level
func NewQuantumZKP(dimensions, securityLevel int, ctx []byte) (*QuantumZKP, error) {
	signer, err := NewSignatureScheme(nil)
	if err != nil {
		return nil, fmt.Errorf("failed to init signature scheme: %w", err)
	}
	return &QuantumZKP{
		Dimensions:    dimensions,
		SecurityLevel: securityLevel,
		Cache:         NewResultCache(),
		Signer:        signer,
	}, nil
}

// Prove generates a proof object for the given state vector
func (q *QuantumZKP) Prove(
	states []complex128,
	identifier string,
	key []byte,
) (*Proof, error) {
	if len(states) == 0 {
		return nil, errors.New("state vector cannot be empty")
	}

	// 1) Create superposition
	superpos := CreateSuperposition(states)

	// 2) Compute metadata
	ent := CalculateEntropy(states)
	meta := StateMetadata{
		Coherence:    ent / float64(len(states)),
		Entanglement: ent,
		Timestamp:    time.Now(),
	}

	// 3) Compute commitment
	commitment := GenerateCommitment(superpos, identifier, key)

	// 4) Generate measurements
	measCount := min(len(states), q.SecurityLevel/8)
	measurements := make([]Measurement, measCount)

	// Pre-compute X-basis states for X measurements
	var xStates []complex128
	var err error
	for i := 0; i < measCount; i++ {
		basis := []string{"Z", "X"}[i%2]
		if basis == "X" && xStates == nil {
			xStates, err = ApplyHadamard(states)
			if err != nil {
				return nil, fmt.Errorf("failed to apply Hadamard: %w", err)
			}
		}
	}

	for i := 0; i < measCount; i++ {
		idx := i % len(states)
		basis := []string{"Z", "X"}[i%2]
		var prob float64
		var phase float64

		if basis == "Z" {
			prob = real(states[idx])*real(states[idx]) + imag(states[idx])*imag(states[idx])
			phase = imag(states[idx])
		} else { // X basis
			prob = real(xStates[idx])*real(xStates[idx]) + imag(xStates[idx])*imag(xStates[idx])
			phase = imag(xStates[idx])
		}

		measurements[i] = Measurement{
			BasisIndex:       idx,
			Probability:      prob,
			Phase:            phase,
			MeasurementBasis: basis,
		}
	}

	// 7) Build final Proof
	proof := &Proof{
		QuantumDimensions: q.Dimensions,
		BasisCoefficients: superpos.CoordinatesAsSlices(),
		Amplitudes:        superpos.Amplitudes,
		Measurements:      measurements,
		StateMetadata:     meta,
		Identifier:        identifier,
		Commitment:        hex.EncodeToString(commitment),
		Signature:         "",
	}

	// compute hex commitment
	rawCommit := GenerateCommitment(superpos, identifier, key) // returns []byte
	commitHex := hex.EncodeToString(rawCommit)
	proof.Commitment = commitHex

	// prep message = JSON(proof without Sig) + commitHex
	temp := *proof
	temp.Signature = ""
	proofBytes, err := json.Marshal(&temp)
	if err != nil {
		return nil, err
	}
	msg := append(proofBytes, []byte(commitHex)...)

	// sign
	sigBytes, err := q.Signer.Sign(msg)
	if err != nil {
		return nil, err
	}
	proof.Signature = hex.EncodeToString(sigBytes)
	return proof, nil
}

// ProveFromBytes generates a proof for data represented as bytes.
// The bytes are converted to a quantum state vector using BytesToState.
// This method ensures deterministic proof generation for the same input bytes.
func (q *QuantumZKP) ProveFromBytes(
	data []byte,
	identifier string,
	key []byte,
) (*Proof, error) {
	// Convert bytes to quantum state vector
	// Use a power of 2 size that's reasonable for the security level
	targetSize := 8 // Default to 8 (2^3) for compatibility with existing tests
	if q.SecurityLevel >= 256 {
		targetSize = 16 // 2^4 for higher security
	}

	states, err := BytesToState(data, targetSize)
	if err != nil {
		return nil, fmt.Errorf("failed to convert bytes to state: %w", err)
	}

	// For deterministic behavior, we need to use a custom implementation
	// that doesn't rely on random amplitudes
	return q.ProveWithDeterministicSuperposition(states, identifier, key)
}

// VerifyProofFromBytes verifies a proof that was generated from bytes.
// This is equivalent to VerifyProof but provides a clearer API for byte-based proofs.
func (q *QuantumZKP) VerifyProofFromBytes(
	proof *Proof,
	key []byte,
) bool {
	return q.VerifyProof(proof, key)
}

// ProveWithDeterministicSuperposition generates a proof using deterministic superposition
// to ensure consistent results for the same input states.
func (q *QuantumZKP) ProveWithDeterministicSuperposition(
	states []complex128,
	identifier string,
	key []byte,
) (*Proof, error) {
	if len(states) == 0 {
		return nil, errors.New("state vector cannot be empty")
	}

	// 1) Create deterministic superposition
	superpos := CreateDeterministicSuperposition(states)

	// 2) Compute metadata
	ent := CalculateEntropy(states)
	meta := StateMetadata{
		Coherence:    ent / float64(len(states)),
		Entanglement: ent,
		Timestamp:    time.Now(),
	}

	// 3) Compute commitment
	commitment := GenerateCommitment(superpos, identifier, key)

	// 4) Generate measurements (same as regular Prove method)
	measCount := min(len(states), q.SecurityLevel/8)
	measurements := make([]Measurement, measCount)

	// Pre-compute X-basis states for X measurements
	var xStates []complex128
	var err error
	for i := 0; i < measCount; i++ {
		basis := []string{"Z", "X"}[i%2]
		if basis == "X" && xStates == nil {
			xStates, err = ApplyHadamard(states)
			if err != nil {
				return nil, fmt.Errorf("failed to apply Hadamard: %w", err)
			}
		}
	}

	for i := 0; i < measCount; i++ {
		idx := i % len(states)
		basis := []string{"Z", "X"}[i%2]
		var prob float64
		var phase float64

		if basis == "Z" {
			prob = real(states[idx])*real(states[idx]) + imag(states[idx])*imag(states[idx])
			phase = imag(states[idx])
		} else { // X basis
			prob = real(xStates[idx])*real(xStates[idx]) + imag(xStates[idx])*imag(xStates[idx])
			phase = imag(xStates[idx])
		}

		measurements[i] = Measurement{
			BasisIndex:       idx,
			Probability:      prob,
			Phase:            phase,
			MeasurementBasis: basis,
		}
	}

	// 5) Build final Proof
	proof := &Proof{
		QuantumDimensions: q.Dimensions,
		BasisCoefficients: superpos.CoordinatesAsSlices(),
		Amplitudes:        superpos.Amplitudes,
		Measurements:      measurements,
		StateMetadata:     meta,
		Identifier:        identifier,
		Commitment:        hex.EncodeToString(commitment),
		Signature:         "",
	}

	// 6) Prepare message and sign
	temp := *proof
	temp.Signature = ""
	proofBytes, err := json.Marshal(&temp)
	if err != nil {
		return nil, err
	}
	msg := append(proofBytes, []byte(proof.Commitment)...)

	sigBytes, err := q.Signer.Sign(msg)
	if err != nil {
		return nil, err
	}
	proof.Signature = hex.EncodeToString(sigBytes)

	return proof, nil
}

// VerifyProof verifies the proof against the commitment
// --- in VerifyProof ---
func (q *QuantumZKP) VerifyProof(
	proof *Proof,
	key []byte,
) bool {
	// 1) Recompute & compare commitment
	states := StatesFromSlices(proof.BasisCoefficients)
	superpos := Superposition{States: states, Amplitudes: proof.Amplitudes}
	rawCommit := GenerateCommitment(superpos, proof.Identifier, key)
	computedCommit := hex.EncodeToString(rawCommit)
	if computedCommit != proof.Commitment {
		return false
	}

	// 2) Rebuild the exact msg bytes
	temp := *proof
	temp.Signature = ""
	proofBytes, err := json.Marshal(&temp)
	if err != nil {
		return false
	}
	msg := append(proofBytes, []byte(proof.Commitment)...)

	// 3) Decode the signature from hex and verify
	sigBytes, err := hex.DecodeString(proof.Signature)
	if err != nil {
		return false
	}
	if !q.Signer.Verify(msg, sigBytes) {
		return false
	}

	// 4) measurements & coefficients…
	if !verifyMeasurements(proof.Measurements, states) {
		return false
	}
	if !verifyCoefficients(states) {
		return false
	}
	return true
}

// StatesFromSlices rebuilds []complex128 from [][]float64
func StatesFromSlices(slices [][]float64) []complex128 {
	cs := make([]complex128, len(slices))
	for i, p := range slices {
		cs[i] = complex(p[0], p[1])
	}
	return cs
}

// min returns the smaller of two ints
func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}
