package main

import (
	"math"
)

// Verify checks if the observed distribution matches the expected amplitudes within epsilon
func Verify(expected Superposition, observed []float64, epsilon float64) bool {
	if len(expected.Amplitudes) != len(observed) {
		return false
	}

	for i := range observed {
		if math.Abs(expected.Amplitudes[i]-observed[i]) > epsilon {
			return false
		}
	}

	return true
}
