# Quantum ZKP API Documentation

**Author:** Nick Cloutier

**ORCID:** 0009-0008-5289-5324

**GitHub:** https://github.com/nicksdigital/

**Affiliation:** Hydra Research & Labs

**Date:** May 24th, 2025

## 🛡️ SecureQuantumZKP (RECOMMENDED)

The secure implementation that provides true zero-knowledge properties.

### Constructor

```go
func NewSecureQuantumZKP(dimensions, securityLevel int, ctx []byte) (*SecureQuantumZKP, error)
```

**Parameters:**
- `dimensions` (int): Quantum system dimensions (recommended: 3-8)
- `securityLevel` (int): Security level in bits (128, 192, or 256)
- `ctx` ([]byte): Application context for domain separation

**Note:** This creates a ZKP with soundness security based on the securityLevel:
- 128-bit → 80-bit soundness (~20KB proofs)
- 192-bit → 96-bit soundness (~22KB proofs)
- 256-bit → 128-bit soundness (~26KB proofs)

**Returns:**
- `*SecureQuantumZKP`: Initialized secure quantum ZKP instance
- `error`: Error if initialization fails

**Example:**
```go
sq, err := NewSecureQuantumZKP(3, 128, []byte("my-app-context"))
```

#### NewSecureQuantumZKPWithSoundness

```go
func NewSecureQuantumZKPWithSoundness(dimensions, securityLevel, soundnessBits int, ctx []byte) (*SecureQuantumZKP, error)
```

Creates a secure quantum ZKP with custom soundness security level.

**Parameters:**
- `dimensions` (int): Quantum system dimensions
- `securityLevel` (int): Cryptographic security level (128, 192, or 256)
- `soundnessBits` (int): Soundness security level (32-256 bits)
- `ctx` ([]byte): Application context

**Example:**
```go
// 96-bit soundness security (~22KB proofs)
sq, err := NewSecureQuantumZKPWithSoundness(3, 128, 96, []byte("context"))
```

#### NewUltraSecureQuantumZKP

```go
func NewUltraSecureQuantumZKP(dimensions, securityLevel int, ctx []byte) (*SecureQuantumZKP, error)
```

Creates a quantum ZKP with maximum 256-bit soundness security.

**Parameters:**
- `dimensions` (int): Quantum system dimensions
- `securityLevel` (int): Cryptographic security level
- `ctx` ([]byte): Application context

**Returns:** ZKP instance with 256-bit soundness (~42KB proofs)

**Example:**
```go
// Ultra-secure for critical applications
sq, err := NewUltraSecureQuantumZKP(3, 256, []byte("ultra-secure-context"))
```

### Core Methods

#### SecureProveVectorKnowledge

```go
func (sq *SecureQuantumZKP) SecureProveVectorKnowledge(
    vector []complex128,
    identifier string,
    key []byte,
) (*SecureProof, error)
```

Generates a zero-knowledge proof of knowledge for a quantum state vector.

**Parameters:**
- `vector` ([]complex128): Quantum state vector (will be normalized)
- `identifier` (string): Unique identifier for this proof
- `key` ([]byte): Authentication key (minimum 32 bytes recommended)

**Returns:**
- `*SecureProof`: Zero-knowledge proof structure
- `error`: Error if proof generation fails

**Security:** This method reveals NOTHING about the input vector.

#### SecureProveFromBytes

```go
func (sq *SecureQuantumZKP) SecureProveFromBytes(
    data []byte,
    identifier string,
    key []byte,
) (*SecureProof, error)
```

Generates a zero-knowledge proof from arbitrary byte data.

**Parameters:**
- `data` ([]byte): Arbitrary data to prove knowledge of
- `identifier` (string): Unique identifier for this proof
- `key` ([]byte): Authentication key

**Returns:**
- `*SecureProof`: Zero-knowledge proof structure
- `error`: Error if proof generation fails

**Security:** This method reveals NOTHING about the input data.

#### VerifySecureProof

```go
func (sq *SecureQuantumZKP) VerifySecureProof(
    proof *SecureProof,
    key []byte,
) bool
```

Verifies a zero-knowledge proof without learning the secret.

**Parameters:**
- `proof` (*SecureProof): Proof to verify
- `key` ([]byte): Authentication key used during proof generation

**Returns:**
- `bool`: True if proof is valid, false otherwise

**Security:** This method learns NOTHING about the original secret.

## 📊 Data Structures

### SecureProof

```go
type SecureProof struct {
    QuantumDimensions int                    `json:"quantum_dimensions"`
    CommitmentHash    string                 `json:"commitment_hash"`
    ChallengeResponse []ChallengeResponse    `json:"challenge_response"`
    MerkleRoot        string                 `json:"merkle_root"`
    StateMetadata     SecureStateMetadata    `json:"state_metadata"`
    Identifier        string                 `json:"identifier"`
    Signature         string                 `json:"signature"`
    Timestamp         time.Time              `json:"timestamp"`
}
```

**Fields:**
- `QuantumDimensions`: Quantum system dimensions
- `CommitmentHash`: Cryptographic commitment to the secret state
- `ChallengeResponse`: Array of challenge-response pairs
- `MerkleRoot`: Merkle tree root for integrity
- `StateMetadata`: Non-revealing metadata bounds
- `Identifier`: Proof identifier
- `Signature`: Digital signature for authenticity
- `Timestamp`: Proof generation timestamp

### ChallengeResponse

```go
type ChallengeResponse struct {
    ChallengeIndex int     `json:"challenge_index"`
    BasisChoice    string  `json:"basis_choice"`
    Response       string  `json:"response"`
    Commitment     string  `json:"commitment"`
    Proof          string  `json:"proof"`
}
```

**Fields:**
- `ChallengeIndex`: Index of the challenged component
- `BasisChoice`: Measurement basis ("Z" or "X")
- `Response`: Cryptographic response (hashed, not revealing)
- `Commitment`: Commitment to the measurement
- `Proof`: Zero-knowledge proof of correctness

### SecureStateMetadata

```go
type SecureStateMetadata struct {
    Dimension        int       `json:"dimension"`
    EntropyBound     float64   `json:"entropy_bound"`
    CoherenceBound   float64   `json:"coherence_bound"`
    Timestamp        time.Time `json:"timestamp"`
    SecurityLevel    int       `json:"security_level"`
}
```

**Fields:**
- `Dimension`: Vector dimension
- `EntropyBound`: Upper bound on entropy (not exact value)
- `CoherenceBound`: Upper bound on coherence (not exact value)
- `Timestamp`: Metadata generation time
- `SecurityLevel`: Security level in bits

## 🔧 Utility Functions

### BytesToState

```go
func BytesToState(data []byte, targetSize int) ([]complex128, error)
```

Converts arbitrary bytes to a normalized quantum state vector.

**Parameters:**
- `data` ([]byte): Input data
- `targetSize` (int): Target vector size (must be power of 2)

**Returns:**
- `[]complex128`: Normalized quantum state vector
- `error`: Error if conversion fails

### NewQuantumStateVector

```go
func NewQuantumStateVector(coordinates []complex128) *QuantumStateVector
```

Creates a quantum state vector with calculated properties.

**Parameters:**
- `coordinates` ([]complex128): State vector coordinates

**Returns:**
- `*QuantumStateVector`: State vector with properties

## 🔄 Quantum Circuit Operations

### BuildCircuit

```go
func (q *QuantumZKP) BuildCircuit(vector []complex128, identifier string) (*QuantumCircuit, error)
```

Builds a quantum circuit encoding the given vector.

### TranspileCircuit

```go
func (q *QuantumZKP) TranspileCircuit(circuit *QuantumCircuit, optimizationLevel int) (*QuantumCircuit, error)
```

Optimizes a quantum circuit.

**Optimization Levels:**
- `0`: No optimization
- `1`: Basic optimization (redundant gate removal)
- `2`: Medium optimization (gate fusion)
- `3`: High optimization (full optimization)

### ApplyNoiseMitigation

```go
func (q *QuantumZKP) ApplyNoiseMitigation(circuit *QuantumCircuit) (*QuantumCircuit, error)
```

Applies noise mitigation techniques (Pauli twirling).

### ExecuteCircuit

```go
func (q *QuantumZKP) ExecuteCircuit(circuit *QuantumCircuit, shots int) (*ExecutionResult, error)
```

Simulates quantum circuit execution.

## ⚠️ Insecure Implementation (DO NOT USE)

### QuantumZKP (INSECURE)

**🚨 WARNING: This implementation leaks complete state information!**

```go
func NewQuantumZKP(dimensions, securityLevel int, ctx []byte) (*QuantumZKP, error)
func (q *QuantumZKP) Prove(states []complex128, identifier string, key []byte) (*Proof, error)
func (q *QuantumZKP) VerifyProof(proof *Proof, key []byte) bool
```

**Security Issues:**
- Exposes complete state vector in `BasisCoefficients`
- Reveals exact measurement probabilities
- Leaks phase information
- NOT zero-knowledge!

**Use Case:** Educational/comparison purposes ONLY.

## 🔒 Security Considerations

### Key Management

- Use cryptographically secure random keys
- Minimum key length: 32 bytes
- Implement proper key rotation
- Store keys securely (HSM, key vault)

### Input Validation

```go
// Validate vector size
if len(vector) == 0 {
    return nil, errors.New("empty vector")
}

// Validate key length
if len(key) < 32 {
    return nil, errors.New("key too short")
}

// Validate identifier
if identifier == "" {
    return nil, errors.New("empty identifier")
}
```

### Error Handling

```go
proof, err := sq.SecureProveVectorKnowledge(vector, id, key)
if err != nil {
    // Log error without exposing sensitive data
    log.Error("Proof generation failed", "error", err.Error())
    return nil, err
}

if !sq.VerifySecureProof(proof, key) {
    return errors.New("proof verification failed")
}
```

## 📈 Performance Guidelines

### Recommended Parameters

| Use Case | Dimensions | Security Level | Expected Performance |
|----------|------------|----------------|---------------------|
| Development | 3 | 128 | ~1ms proof generation |
| Production | 3-4 | 128 | ~2-5ms proof generation |
| High Security | 4-6 | 256 | ~10-20ms proof generation |
| Research | 6-8 | 256 | ~50-100ms proof generation |

### Optimization Tips

1. **Batch Operations**: Generate multiple proofs in parallel
2. **Caching**: Cache quantum state vectors when possible
3. **Circuit Optimization**: Use appropriate optimization levels
4. **Memory Management**: Reuse proof structures

### Memory Usage

- Secure proof size: ~45KB (typical)
- Memory per proof generation: ~1-5MB
- Recommended: 8GB+ RAM for high-throughput applications

## 🧪 Testing

### Unit Tests

```bash
# Run all tests
go test -v

# Run security tests only
go test -v -run TestSecure

# Run performance benchmarks
go test -bench=.
```

### Integration Testing

```go
func TestIntegration(t *testing.T) {
    sq, _ := NewSecureQuantumZKP(3, 128, []byte("test"))

    vector := []complex128{complex(1, 0), complex(0, 0)}
    key := []byte("test-key-32-bytes-long-enough!!")

    proof, err := sq.SecureProveVectorKnowledge(vector, "test", key)
    assert.NoError(t, err)

    valid := sq.VerifySecureProof(proof, key)
    assert.True(t, valid)
}
```

## 📚 References

### Academic Papers
- Watrous, J. (2009). Zero-knowledge against quantum attacks. SIAM Journal on Computing, 39(1), 25-58.
- Broadbent, A., & Schaffner, C. (2016). Quantum cryptography beyond quantum key distribution.
- Coladangelo, A., et al. (2020). Non-interactive zero-knowledge arguments for QMA, with preprocessing.

### Standards and Specifications
- **NIST Post-Quantum Cryptography**: https://csrc.nist.gov/projects/post-quantum-cryptography
- **CRYSTALS-Dilithium**: https://pq-crystals.org/dilithium/
- **BLAKE3 Cryptographic Hash**: https://github.com/BLAKE3-team/BLAKE3
- **BSI TR-02102**: https://www.bsi.bund.de/EN/Themen/Unternehmen-und-Organisationen/Standards-und-Zertifizierung/Technische-Richtlinien/TR-nach-Thema-sortiert/tr02102/tr02102_node.html

### Security Guidelines
- **NSA CNSA Suite 2.0**: https://www.nsa.gov/Cybersecurity/Post-Quantum-Cybersecurity-Resources/
- **ETSI Quantum Cryptography**: https://www.etsi.org/technologies/quantum-safe-cryptography
- **Cloudflare Post-Quantum**: https://blog.cloudflare.com/pq-2024/
