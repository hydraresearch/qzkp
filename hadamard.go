package main

import (
	"errors"
	"math"
)

// ApplyHadamard applies a full n-qubit Hadamard transform to the state vector.
// The state vector length must be a power of two.
// It returns a new state vector resulting from H^{\otimes n} |psi>.
func ApplyHadamard(state []complex128) ([]complex128, error) {
	N := len(state)
	// Validate length is power of two
	if N == 0 || (N&(N-1)) != 0 {
		return nil, errors.New("state vector length must be a power of two")
	}
	// Compute number of qubits
	numQubits := int(math.Log2(float64(N)))

	// Copy initial state
	result := make([]complex128, N)
	copy(result, state)

	// 1/sqrt(2) factor
	invSqrt2 := 1 / math.Sqrt2

	// Apply single-qubit Hadamard on each qubit iteratively
	for q := 0; q < numQubits; q++ {
		stride := 1 << (q + 1)
		half := 1 << q
		for i := 0; i < N; i += stride {
			for j := 0; j < half; j++ {
				a := result[i+j]
				b := result[i+j+half]

				// H acting on this qubit: (|0>+|1>)/sqrt(2), (|0>-|1>)/sqrt(2)
				result[i+j] = (a + b) * complex(invSqrt2, 0)
				result[i+j+half] = (a - b) * complex(invSqrt2, 0)
			}
		}
	}

	return result, nil
}
