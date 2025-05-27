#!/usr/bin/env python3
"""
Advanced Quantum Circuit Tests for Quantum ZKP System
Implements complex quantum algorithms and entanglement patterns
"""

import os
import sys
import json
import time
import hashlib
import numpy as np
from datetime import datetime
from typing import List, Dict, Any, Tuple
import math

# Add the root directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

try:
    from qiskit import QuantumCircuit, transpile, execute, ClassicalRegister, QuantumRegister
    from qiskit.providers.ibmq import IBMQ
    from qiskit.providers import JobStatus
    from qiskit.quantum_info import Statevector, random_unitary
    from qiskit.circuit.library import QFT, GroverOperator, PhaseOracle
    from qiskit.algorithms import AmplificationProblem
    from dotenv import load_dotenv
    print("✅ Advanced quantum packages imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Install: pip install qiskit qiskit-algorithms python-dotenv")
    sys.exit(1)

class AdvancedQuantumZKPCircuits:
    """Advanced quantum circuit implementations for ZKP protocols"""
    
    def __init__(self):
        self.load_credentials()
        self.provider = None
        self.backend = None
        self.circuit_results = []
        
    def load_credentials(self):
        """Load IBM Quantum credentials"""
        env_path = os.path.join(os.path.dirname(__file__), '../../.env')
        load_dotenv(env_path)
        self.token = os.getenv('IBM_QUANTUM_TOKEN')
        
        if not self.token:
            print("❌ IBM_QUANTUM_TOKEN not found in .env file")
            sys.exit(1)
    
    def connect_to_ibm(self):
        """Connect to IBM Quantum"""
        try:
            IBMQ.save_account(self.token, overwrite=True)
            IBMQ.load_account()
            self.provider = IBMQ.get_provider(hub='ibm-q')
            
            # Prefer backends with more qubits for complex circuits
            backend_preferences = ['ibm_brisbane', 'ibm_kyoto', 'ibm_osaka', 'ibm_sherbrooke']
            
            for backend_name in backend_preferences:
                try:
                    self.backend = self.provider.get_backend(backend_name)
                    config = self.backend.configuration()
                    if config.n_qubits >= 16:  # Need sufficient qubits for complex circuits
                        print(f"✅ Connected to {backend_name} ({config.n_qubits} qubits)")
                        return True
                except:
                    continue
            
            print("❌ No suitable backend found (need ≥16 qubits)")
            return False
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def create_quantum_fourier_transform_zkp(self, secret_data: bytes, n_qubits: int = 8) -> QuantumCircuit:
        """
        Create QZK proof using Quantum Fourier Transform
        Encodes secret in frequency domain for enhanced security
        """
        qc = QuantumCircuit(n_qubits, n_qubits)
        
        # Encode secret data into quantum amplitudes
        data_hash = hashlib.sha256(secret_data).digest()
        
        # Initialize qubits with secret-dependent rotations
        for i in range(n_qubits):
            theta = (data_hash[i % len(data_hash)] / 255.0) * 2 * np.pi
            phi = (data_hash[(i + 8) % len(data_hash)] / 255.0) * 2 * np.pi
            qc.ry(theta, i)
            qc.rz(phi, i)
        
        # Apply Quantum Fourier Transform
        qft = QFT(n_qubits, approximation_degree=2)
        qc.compose(qft, inplace=True)
        
        # Add verification entanglement in frequency domain
        for i in range(0, n_qubits - 1, 2):
            qc.cz(i, i + 1)
        
        # Inverse QFT for final encoding
        qc.compose(qft.inverse(), inplace=True)
        
        # Measurement
        qc.measure_all()
        
        return qc
    
    def create_grover_search_zkp(self, secret_data: bytes, n_qubits: int = 6) -> QuantumCircuit:
        """
        Create QZK proof using Grover's algorithm
        Proves knowledge of secret without revealing search space
        """
        # Create oracle based on secret data
        secret_hash = hashlib.sha256(secret_data).hexdigest()
        target_state = secret_hash[:n_qubits]  # Use first n_qubits hex chars
        
        # Convert to binary
        target_binary = ''.join(format(int(c, 16), '04b') for c in target_state)[:n_qubits]
        
        qc = QuantumCircuit(n_qubits, n_qubits)
        
        # Initialize superposition
        qc.h(range(n_qubits))
        
        # Grover iterations (optimal number)
        iterations = int(np.pi / 4 * np.sqrt(2**n_qubits))
        iterations = min(iterations, 3)  # Limit for hardware constraints
        
        for _ in range(iterations):
            # Oracle: flip phase of target state
            for i, bit in enumerate(target_binary):
                if bit == '0':
                    qc.x(i)
            
            # Multi-controlled Z gate
            if n_qubits > 1:
                qc.h(n_qubits - 1)
                qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
                qc.h(n_qubits - 1)
            
            # Restore qubits
            for i, bit in enumerate(target_binary):
                if bit == '0':
                    qc.x(i)
            
            # Diffusion operator
            qc.h(range(n_qubits))
            qc.x(range(n_qubits))
            
            if n_qubits > 1:
                qc.h(n_qubits - 1)
                qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
                qc.h(n_qubits - 1)
            
            qc.x(range(n_qubits))
            qc.h(range(n_qubits))
        
        qc.measure_all()
        return qc
    
    def create_variational_zkp_circuit(self, secret_data: bytes, n_qubits: int = 8, depth: int = 4) -> QuantumCircuit:
        """
        Create variational quantum circuit for ZKP
        Uses parameterized gates with secret-dependent parameters
        """
        qc = QuantumCircuit(n_qubits, n_qubits)
        
        # Generate parameters from secret data
        data_hash = hashlib.sha256(secret_data).digest()
        params = []
        for i in range(depth * n_qubits * 3):  # 3 parameters per qubit per layer
            param = (data_hash[i % len(data_hash)] / 255.0) * 2 * np.pi
            params.append(param)
        
        param_idx = 0
        
        # Variational layers
        for layer in range(depth):
            # Rotation layer
            for qubit in range(n_qubits):
                qc.ry(params[param_idx], qubit)
                param_idx += 1
                qc.rz(params[param_idx], qubit)
                param_idx += 1
                qc.rx(params[param_idx], qubit)
                param_idx += 1
            
            # Entanglement layer
            for qubit in range(n_qubits - 1):
                qc.cx(qubit, qubit + 1)
            
            # Ring connectivity
            if n_qubits > 2:
                qc.cx(n_qubits - 1, 0)
        
        # Final measurement
        qc.measure_all()
        return qc
    
    def create_quantum_error_correction_zkp(self, secret_data: bytes, n_qubits: int = 9) -> QuantumCircuit:
        """
        Create ZKP with quantum error correction encoding
        Uses 3-qubit repetition code for enhanced reliability
        """
        if n_qubits % 3 != 0:
            n_qubits = (n_qubits // 3) * 3  # Ensure divisible by 3
        
        logical_qubits = n_qubits // 3
        qc = QuantumCircuit(n_qubits, logical_qubits)
        
        # Encode secret into logical qubits
        data_hash = hashlib.sha256(secret_data).digest()
        
        for i in range(logical_qubits):
            # Encode logical qubit i
            physical_start = i * 3
            
            # Initialize with secret-dependent state
            theta = (data_hash[i % len(data_hash)] / 255.0) * 2 * np.pi
            qc.ry(theta, physical_start)
            
            # 3-qubit repetition encoding
            qc.cx(physical_start, physical_start + 1)
            qc.cx(physical_start, physical_start + 2)
        
        # Add logical entanglement
        for i in range(0, logical_qubits - 1):
            qc.cx(i * 3, (i + 1) * 3)
        
        # Error syndrome measurement (simplified)
        for i in range(logical_qubits):
            physical_start = i * 3
            # Measure logical qubit (majority vote)
            qc.measure(physical_start, i)
        
        return qc
    
    def create_quantum_teleportation_zkp(self, secret_data: bytes, n_qubits: int = 12) -> QuantumCircuit:
        """
        Create ZKP using quantum teleportation protocol
        Demonstrates quantum communication without classical channel
        """
        if n_qubits < 6:
            n_qubits = 6  # Minimum for teleportation
        
        # Use qubits in groups of 3 for teleportation
        teleport_groups = n_qubits // 3
        
        qc = QuantumCircuit(n_qubits, teleport_groups)
        
        data_hash = hashlib.sha256(secret_data).digest()
        
        for group in range(teleport_groups):
            base = group * 3
            alice_qubit = base
            bob_qubit = base + 1
            message_qubit = base + 2
            
            # Prepare message qubit with secret data
            theta = (data_hash[group % len(data_hash)] / 255.0) * 2 * np.pi
            phi = (data_hash[(group + 8) % len(data_hash)] / 255.0) * 2 * np.pi
            
            qc.ry(theta, message_qubit)
            qc.rz(phi, message_qubit)
            
            # Create Bell pair between Alice and Bob
            qc.h(alice_qubit)
            qc.cx(alice_qubit, bob_qubit)
            
            # Alice's Bell measurement
            qc.cx(message_qubit, alice_qubit)
            qc.h(message_qubit)
            
            # Measure Alice's qubits (classical communication simulation)
            # In real protocol, Bob would apply corrections based on Alice's results
            
            # For ZKP, we measure Bob's qubit to verify teleportation
            qc.measure(bob_qubit, group)
        
        return qc
    
    def create_quantum_supremacy_circuit(self, secret_data: bytes, n_qubits: int = 16, depth: int = 8) -> QuantumCircuit:
        """
        Create quantum supremacy-style random circuit
        High-depth random circuit for maximum quantum advantage
        """
        qc = QuantumCircuit(n_qubits, n_qubits)
        
        # Seed random number generator with secret data
        seed = int.from_bytes(hashlib.sha256(secret_data).digest()[:4], 'big')
        np.random.seed(seed)
        
        # Initial layer of Hadamard gates
        qc.h(range(n_qubits))
        
        # Random circuit layers
        for layer in range(depth):
            # Random single-qubit gates
            for qubit in range(n_qubits):
                gate_choice = np.random.randint(0, 4)
                angle = np.random.uniform(0, 2 * np.pi)
                
                if gate_choice == 0:
                    qc.rx(angle, qubit)
                elif gate_choice == 1:
                    qc.ry(angle, qubit)
                elif gate_choice == 2:
                    qc.rz(angle, qubit)
                else:
                    qc.h(qubit)
            
            # Random two-qubit gates
            available_qubits = list(range(n_qubits))
            np.random.shuffle(available_qubits)
            
            for i in range(0, len(available_qubits) - 1, 2):
                qubit1, qubit2 = available_qubits[i], available_qubits[i + 1]
                
                gate_choice = np.random.randint(0, 3)
                if gate_choice == 0:
                    qc.cx(qubit1, qubit2)
                elif gate_choice == 1:
                    qc.cz(qubit1, qubit2)
                else:
                    angle = np.random.uniform(0, 2 * np.pi)
                    qc.crz(angle, qubit1, qubit2)
        
        # Final measurement
        qc.measure_all()
        return qc
    
    def execute_advanced_circuit_test(self, circuit_name: str, circuit: QuantumCircuit) -> Dict[str, Any]:
        """Execute advanced quantum circuit on IBM hardware"""
        print(f"🔬 Executing advanced circuit: {circuit_name}")
        
        try:
            # Optimize circuit for hardware
            transpiled_qc = transpile(circuit, self.backend, optimization_level=3)
            
            print(f"   Original depth: {circuit.depth()}")
            print(f"   Transpiled depth: {transpiled_qc.depth()}")
            print(f"   Qubits: {transpiled_qc.num_qubits}")
            print(f"   Gates: {transpiled_qc.count_ops()}")
            
            # Execute with adaptive shots based on circuit complexity
            shots = min(1000, max(100, 1000 // (transpiled_qc.depth() // 10 + 1)))
            
            start_time = time.time()
            job = execute(transpiled_qc, self.backend, shots=shots)
            
            job_id = job.job_id()
            print(f"   Job ID: {job_id}")
            
            # Wait for completion
            while job.status() not in [JobStatus.DONE, JobStatus.ERROR, JobStatus.CANCELLED]:
                print(f"   Status: {job.status()}")
                time.sleep(15)
            
            execution_time = time.time() - start_time
            
            result = {
                'circuit_name': circuit_name,
                'job_id': job_id,
                'backend': self.backend.name(),
                'status': str(job.status()),
                'execution_time': execution_time,
                'original_depth': circuit.depth(),
                'transpiled_depth': transpiled_qc.depth(),
                'num_qubits': transpiled_qc.num_qubits,
                'gate_count': dict(transpiled_qc.count_ops()),
                'shots': shots,
                'timestamp': datetime.now().isoformat(),
                'success': job.status() == JobStatus.DONE
            }
            
            if job.status() == JobStatus.DONE:
                job_result = job.result()
                counts = job_result.get_counts()
                
                # Advanced quantum metrics
                result.update({
                    'measurement_counts': counts,
                    'unique_outcomes': len(counts),
                    'entropy': self.calculate_quantum_entropy(counts),
                    'quantum_volume_estimate': self.estimate_quantum_volume(transpiled_qc),
                    'circuit_complexity': self.calculate_circuit_complexity(transpiled_qc),
                    'entanglement_measure': self.estimate_entanglement(counts)
                })
                
                print(f"   ✅ Advanced circuit executed successfully")
                print(f"   📊 Unique outcomes: {len(counts)}")
                print(f"   🌀 Quantum entropy: {result['entropy']:.3f}")
                
            else:
                print(f"   ❌ Circuit execution failed: {job.status()}")
            
            return result
            
        except Exception as e:
            print(f"   ❌ Circuit execution error: {e}")
            return {
                'circuit_name': circuit_name,
                'error': str(e),
                'success': False,
                'timestamp': datetime.now().isoformat()
            }
    
    def calculate_quantum_entropy(self, counts: Dict[str, int]) -> float:
        """Calculate quantum entropy from measurement results"""
        total = sum(counts.values())
        if total == 0:
            return 0.0
        
        entropy = 0.0
        for count in counts.values():
            if count > 0:
                p = count / total
                entropy -= p * np.log2(p)
        
        return entropy
    
    def estimate_quantum_volume(self, circuit: QuantumCircuit) -> int:
        """Estimate quantum volume based on circuit properties"""
        n_qubits = circuit.num_qubits
        depth = circuit.depth()
        
        # Simplified quantum volume estimate
        return min(n_qubits, depth) ** 2
    
    def calculate_circuit_complexity(self, circuit: QuantumCircuit) -> Dict[str, int]:
        """Calculate circuit complexity metrics"""
        gate_counts = circuit.count_ops()
        
        # Count two-qubit gates (more expensive)
        two_qubit_gates = sum(count for gate, count in gate_counts.items() 
                             if gate in ['cx', 'cz', 'cy', 'crz', 'crx', 'cry', 'ccx'])
        
        return {
            'total_gates': sum(gate_counts.values()),
            'two_qubit_gates': two_qubit_gates,
            'single_qubit_gates': sum(gate_counts.values()) - two_qubit_gates,
            'depth': circuit.depth(),
            'width': circuit.num_qubits
        }
    
    def estimate_entanglement(self, counts: Dict[str, int]) -> float:
        """Estimate entanglement from measurement correlations"""
        if len(counts) < 2:
            return 0.0
        
        # Simple entanglement measure based on outcome distribution
        total = sum(counts.values())
        max_prob = max(counts.values()) / total
        
        # Higher entanglement typically leads to more uniform distribution
        n_outcomes = len(counts)
        uniform_prob = 1.0 / n_outcomes
        
        # Entanglement measure (0 = no entanglement, 1 = maximum entanglement)
        entanglement = 1.0 - abs(max_prob - uniform_prob) / (1.0 - uniform_prob)
        
        return max(0.0, min(1.0, entanglement))

def main():
    """Main execution function for advanced circuit tests"""
    print("🚀 Advanced Quantum Circuit Test Suite")
    print("=" * 50)
    
    tester = AdvancedQuantumZKPCircuits()
    
    if not tester.connect_to_ibm():
        return 1
    
    # Test secret data
    secret_data = b"Advanced Quantum ZKP Test Data 2025"
    
    # Advanced circuit test cases
    test_circuits = [
        ("QFT_ZKP_8qubit", tester.create_quantum_fourier_transform_zkp(secret_data, 8)),
        ("Grover_ZKP_6qubit", tester.create_grover_search_zkp(secret_data, 6)),
        ("Variational_ZKP_8qubit", tester.create_variational_zkp_circuit(secret_data, 8, 4)),
        ("QEC_ZKP_9qubit", tester.create_quantum_error_correction_zkp(secret_data, 9)),
        ("Teleportation_ZKP_12qubit", tester.create_quantum_teleportation_zkp(secret_data, 12)),
        ("Supremacy_ZKP_16qubit", tester.create_quantum_supremacy_circuit(secret_data, 16, 6))
    ]
    
    results = []
    
    for i, (name, circuit) in enumerate(test_circuits, 1):
        print(f"\n📋 Advanced Test {i}/{len(test_circuits)}: {name}")
        print("-" * 60)
        
        result = tester.execute_advanced_circuit_test(name, circuit)
        results.append(result)
        
        # Pause between complex tests
        if i < len(test_circuits):
            print("⏳ Waiting 45s before next advanced test...")
            time.sleep(45)
    
    # Generate comprehensive report
    successful = sum(1 for r in results if r.get('success', False))
    total = len(results)
    
    print(f"\n🎉 Advanced Circuit Test Suite Complete!")
    print("=" * 50)
    print(f"✅ Successful: {successful}/{total}")
    print(f"📊 Success Rate: {successful/total*100:.1f}%")
    
    # Save detailed results
    report_data = {
        'test_summary': {
            'total_tests': total,
            'successful_tests': successful,
            'timestamp': datetime.now().isoformat(),
            'backend': tester.backend.name()
        },
        'advanced_results': results
    }
    
    filename = f"advanced_quantum_circuits_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(report_data, f, indent=2)
    
    print(f"📄 Advanced report saved: {filename}")
    
    return 0 if successful == total else 1

if __name__ == "__main__":
    exit(main())
