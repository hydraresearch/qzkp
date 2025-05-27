package main

import (
	"fmt"
	"runtime"
	"time"
	"github.com/hydraresearch/qzkp/src/classical"
)

func main() {
	fmt.Println("Memory Usage Analysis")
	fmt.Println("====================")
	
	// Force GC before starting
	runtime.GC()
	
	var m1, m2 runtime.MemStats
	runtime.ReadMemStats(&m1)
	
	// Perform operations
	iterations := 1000
	for i := 0; i < iterations; i++ {
		testData := []byte("memory test data")
		states, _ := classical.BytesToState(testData, 4)
		superpos := classical.CreateSuperposition(states)
		key := []byte("memory-test-key-32bytes-length")
		classical.GenerateCommitment(superpos, "memory", key)
	}
	
	runtime.ReadMemStats(&m2)
	
	fmt.Printf("Iterations: %d\n", iterations)
	fmt.Printf("Memory before: %d KB\n", m1.Alloc/1024)
	fmt.Printf("Memory after: %d KB\n", m2.Alloc/1024)
	fmt.Printf("Memory used: %d KB\n", (m2.Alloc-m1.Alloc)/1024)
	fmt.Printf("Memory per operation: %d bytes\n", (m2.Alloc-m1.Alloc)/uint64(iterations))
	fmt.Printf("Total allocations: %d\n", m2.TotalAlloc/1024)
	fmt.Printf("GC cycles: %d\n", m2.NumGC)
}
