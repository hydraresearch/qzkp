package main

import (
	"encoding/json"
	"fmt"
	"os"
	"time"
)

// QuantumStateCache manages local storage of real quantum states
type QuantumStateCache struct {
	FilePath string
}

// CachedQuantumState represents a cached quantum state with metadata
type CachedQuantumState struct {
	Vector      []complex128          `json:"vector"`
	Name        string                `json:"name"`
	Description string                `json:"description"`
	Qubits      int                   `json:"qubits"`
	Backend     string                `json:"backend"`
	Timestamp   time.Time             `json:"timestamp"`
	Metadata    map[string]interface{} `json:"metadata"`
	Fidelity    float64               `json:"fidelity"`
	Coherence   float64               `json:"coherence"`
	Entanglement float64              `json:"entanglement"`
	JobID       string                `json:"job_id,omitempty"`
}

// QuantumStateLibrary contains a collection of cached quantum states
type QuantumStateLibrary struct {
	States    []CachedQuantumState `json:"states"`
	Generated time.Time            `json:"generated"`
	Version   string               `json:"version"`
	TotalJobs int                  `json:"total_jobs"`
	UsedTime  float64              `json:"used_time_seconds"` // Track quantum time usage
}

// NewQuantumStateCache creates a new cache instance
func NewQuantumStateCache(filePath string) (*QuantumStateCache, error) {
	return &QuantumStateCache{
		FilePath: filePath,
	}, nil
}

// LoadStateLibrary loads the quantum state library from cache
func (cache *QuantumStateCache) LoadStateLibrary() (*QuantumStateLibrary, error) {
	if _, err := os.Stat(cache.FilePath); os.IsNotExist(err) {
		// Return empty library if file doesn't exist
		return &QuantumStateLibrary{
			States:    make([]CachedQuantumState, 0),
			Generated: time.Now(),
			Version:   "1.0",
			TotalJobs: 0,
			UsedTime:  0.0,
		}, nil
	}

	data, err := os.ReadFile(cache.FilePath)
	if err != nil {
		return nil, fmt.Errorf("failed to read cache file: %v", err)
	}

	var library QuantumStateLibrary
	if err := json.Unmarshal(data, &library); err != nil {
		return nil, fmt.Errorf("failed to unmarshal cache data: %v", err)
	}

	return &library, nil
}

// SaveStateLibrary saves the quantum state library to cache
func (cache *QuantumStateCache) SaveStateLibrary(library *QuantumStateLibrary) error {
	data, err := json.MarshalIndent(library, "", "  ")
	if err != nil {
		return fmt.Errorf("failed to marshal library: %v", err)
	}

	if err := os.WriteFile(cache.FilePath, data, 0644); err != nil {
		return fmt.Errorf("failed to write cache file: %v", err)
	}

	fmt.Printf("💾 Saved %d quantum states to cache (%s)\n", len(library.States), cache.FilePath)
	return nil
}

// AddState adds a new quantum state to the cache
func (cache *QuantumStateCache) AddState(state CachedQuantumState) error {
	library, err := cache.LoadStateLibrary()
	if err != nil {
		return err
	}

	// Check if state already exists (by name)
	for i, existing := range library.States {
		if existing.Name == state.Name {
			// Update existing state
			library.States[i] = state
			return cache.SaveStateLibrary(library)
		}
	}

	// Add new state
	library.States = append(library.States, state)
	library.TotalJobs++
	
	return cache.SaveStateLibrary(library)
}

// GetStatesByQubits returns all cached states with the specified number of qubits
func (cache *QuantumStateCache) GetStatesByQubits(qubits int) ([]CachedQuantumState, error) {
	library, err := cache.LoadStateLibrary()
	if err != nil {
		return nil, err
	}

	var filtered []CachedQuantumState
	for _, state := range library.States {
		if state.Qubits == qubits {
			filtered = append(filtered, state)
		}
	}

	return filtered, nil
}

// GetStatesByType returns all cached states matching the specified type/name pattern
func (cache *QuantumStateCache) GetStatesByType(stateType string) ([]CachedQuantumState, error) {
	library, err := cache.LoadStateLibrary()
	if err != nil {
		return nil, err
	}

	var filtered []CachedQuantumState
	for _, state := range library.States {
		if stateType == "all" || state.Name == stateType {
			filtered = append(filtered, state)
		}
	}

	return filtered, nil
}

// GetUsageStats returns statistics about quantum time usage
func (cache *QuantumStateCache) GetUsageStats() (*QuantumUsageStats, error) {
	library, err := cache.LoadStateLibrary()
	if err != nil {
		return nil, err
	}

	stats := &QuantumUsageStats{
		TotalStates:     len(library.States),
		TotalJobs:       library.TotalJobs,
		UsedTimeSeconds: library.UsedTime,
		LastGenerated:   library.Generated,
		StatesByQubits:  make(map[int]int),
		StatesByType:    make(map[string]int),
	}

	for _, state := range library.States {
		stats.StatesByQubits[state.Qubits]++
		stats.StatesByType[state.Name]++
	}

	return stats, nil
}

// QuantumUsageStats provides statistics about cached quantum states
type QuantumUsageStats struct {
	TotalStates     int            `json:"total_states"`
	TotalJobs       int            `json:"total_jobs"`
	UsedTimeSeconds float64        `json:"used_time_seconds"`
	LastGenerated   time.Time      `json:"last_generated"`
	StatesByQubits  map[int]int    `json:"states_by_qubits"`
	StatesByType    map[string]int `json:"states_by_type"`
}

// UpdateUsageTime adds to the total quantum time used
func (cache *QuantumStateCache) UpdateUsageTime(additionalSeconds float64) error {
	library, err := cache.LoadStateLibrary()
	if err != nil {
		return err
	}

	library.UsedTime += additionalSeconds
	return cache.SaveStateLibrary(library)
}

// ClearCache removes all cached states (use with caution!)
func (cache *QuantumStateCache) ClearCache() error {
	if err := os.Remove(cache.FilePath); err != nil && !os.IsNotExist(err) {
		return fmt.Errorf("failed to remove cache file: %v", err)
	}
	
	fmt.Println("🗑️  Cache cleared successfully")
	return nil
}

// ExportStates exports cached states to a different format
func (cache *QuantumStateCache) ExportStates(outputPath string, format string) error {
	library, err := cache.LoadStateLibrary()
	if err != nil {
		return err
	}

	switch format {
	case "json":
		return cache.exportAsJSON(library, outputPath)
	case "csv":
		return cache.exportAsCSV(library, outputPath)
	default:
		return fmt.Errorf("unsupported export format: %s", format)
	}
}

// exportAsJSON exports states as JSON
func (cache *QuantumStateCache) exportAsJSON(library *QuantumStateLibrary, outputPath string) error {
	data, err := json.MarshalIndent(library, "", "  ")
	if err != nil {
		return err
	}
	
	return os.WriteFile(outputPath, data, 0644)
}

// exportAsCSV exports states as CSV (simplified)
func (cache *QuantumStateCache) exportAsCSV(library *QuantumStateLibrary, outputPath string) error {
	// This is a simplified CSV export - in practice you'd want more sophisticated formatting
	csvContent := "name,qubits,backend,fidelity,coherence,entanglement,timestamp\n"
	
	for _, state := range library.States {
		csvContent += fmt.Sprintf("%s,%d,%s,%.6f,%.6f,%.6f,%s\n",
			state.Name, state.Qubits, state.Backend,
			state.Fidelity, state.Coherence, state.Entanglement,
			state.Timestamp.Format(time.RFC3339))
	}
	
	return os.WriteFile(outputPath, []byte(csvContent), 0644)
}

// PrintCacheInfo displays information about the current cache
func (cache *QuantumStateCache) PrintCacheInfo() error {
	stats, err := cache.GetUsageStats()
	if err != nil {
		return err
	}

	fmt.Println("📊 Quantum State Cache Information:")
	fmt.Printf("   Total States: %d\n", stats.TotalStates)
	fmt.Printf("   Total Jobs: %d\n", stats.TotalJobs)
	fmt.Printf("   Used Time: %.2f seconds (%.2f minutes)\n", stats.UsedTimeSeconds, stats.UsedTimeSeconds/60)
	fmt.Printf("   Last Generated: %s\n", stats.LastGenerated.Format(time.RFC3339))
	
	fmt.Println("   States by Qubits:")
	for qubits, count := range stats.StatesByQubits {
		fmt.Printf("     %d qubits: %d states\n", qubits, count)
	}
	
	fmt.Println("   States by Type:")
	for stateType, count := range stats.StatesByType {
		fmt.Printf("     %s: %d states\n", stateType, count)
	}

	return nil
}
