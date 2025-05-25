package main

import (
	"math"
)

// Measurement holds a single quantum measurement result.

// GenerateMeasurements creates a list of measurements by sampling probabilities from the state vector.
func GenerateMeasurements(states []complex128, num int) []Measurement {
	measurements := make([]Measurement, num)
	n := len(states)
	for i := 0; i < num; i++ {
		idx := i % n // Cycle through coordinates safely
		measurements[i] = Measurement{
			BasisIndex:       idx,
			Probability:      real(states[idx])*real(states[idx]) + imag(states[idx])*imag(states[idx]),
			Phase:            imag(states[idx]),
			MeasurementBasis: []string{"Z", "X"}[i%2],
		}
	}
	return measurements
}

// verifyMeasurements checks whether each measurement matches
// the theoretical probability for Z- and X-basis (using Hadamard).
func verifyMeasurements(meas []Measurement, states []complex128) bool {
	const tol = 1e-5
	var xStates []complex128
	for _, m := range meas {
		idx := m.BasisIndex
		if idx < 0 || idx >= len(states) {
			return false
		}
		// Z-basis
		if m.MeasurementBasis == "Z" {
			theor := real(states[idx])*real(states[idx]) + imag(states[idx])*imag(states[idx])
			if math.Abs(theor-m.Probability) > tol {
				return false
			}
		} else if m.MeasurementBasis == "X" {
			// compute X-basis only once
			if xStates == nil {
				var err error
				xStates, err = ApplyHadamard(states)
				if err != nil {
					return false
				}
			}
			theor := real(xStates[idx])*real(xStates[idx]) + imag(xStates[idx])*imag(xStates[idx])
			if math.Abs(theor-m.Probability) > tol {
				return false
			}
		} else {
			// unknown basis
			return false
		}
	}
	return true
}

// verifyCoefficients checks that the state vector is normalized: sum(|c|^2)=1
func verifyCoefficients(states []complex128) bool {
	const tol = 1e-10
	var sum float64
	for _, c := range states {
		r := real(c)
		i := imag(c)
		sum += r*r + i*i
	}
	return math.Abs(sum-1.0) < tol
}
