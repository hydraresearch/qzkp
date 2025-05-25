package main

import (
	"math"
	"math/cmplx"
)

func CalculateEntropy(coords []complex128) float64 {
	var entropy float64
	for _, c := range coords {
		p := cmplx.Abs(c) * cmplx.Abs(c)
		if p > 0 {
			entropy -= p * math.Log2(p)
		}
	}
	return entropy
}
