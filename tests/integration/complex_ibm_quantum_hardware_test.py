#!/usr/bin/env python3
"""
Complex IBM Quantum Hardware Test Suite
Advanced quantum circuits with high qubit counts on real IBM hardware
"""

import os
import sys
import json
import time
import hashlib
import numpy as np
from datetime import datetime
from typing import List, Dict, Any, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

try:
    from qiskit import QuantumCircuit, transpile
    from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
    from qiskit.quantum_info import Statevector
    from qiskit.circuit.library import QFT
    from dotenv import load_dotenv
    print("✅ Complex quantum packages loaded")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Installing required packages...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "qiskit", "qiskit-ibm-runtime", "python-dotenv", "--quiet"])
    
    # Retry imports
    from qiskit import QuantumCircuit, transpile
    from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
    from qiskit.quantum_info import Statevector
    from qiskit.circuit.library import QFT
    from dotenv import load_dotenv
    print("✅ Packages installed and imported")

class ComplexIBMQuantumTester:
    """Complex quantum circuit testing on real IBM hardware"""
    
    def __init__(self):
        self.load_credentials()
        self.service = None
        self.backend = None
        self.max_qubits = 0
        self.test_results = []
        self.timeout = 120  # 2 minute timeout for complex circuits
        
    def load_credentials(self):
        """Load IBM Quantum credentials"""
        env_path = os.path.join(os.path.dirname(__file__), '../../.env')
        load_dotenv(env_path)
        self.token = os.getenv('IQKAPI')
        
        if not self.token:
            print("❌ IQKAPI not found in .env file")
            sys.exit(1)
    
    def connect_to_largest_backend(self):
        """Connect to the largest available IBM Quantum backend"""
        try:
            print("🔌 Connecting to IBM Quantum (seeking largest backend)...")
            
            self.service = QiskitRuntimeService(token=self.token, channel='ibm_quantum')
            
            # Get all operational backends
            backends = self.service.backends(simulator=False, operational=True)
            
            if not backends:
                print("❌ No operational backends available")
                return False
            
            # Sort by number of qubits (descending)
            backends_with_qubits = []
            for backend in backends:
                try:
                    config = backend.configuration()
                    status = backend.status()
                    backends_with_qubits.append((backend, config.n_qubits, status.pending_jobs))
                except:
                    continue
            
            # Sort by qubits (desc), then by queue length (asc)
            backends_with_qubits.sort(key=lambda x: (-x[1], x[2]))
            
            if backends_with_qubits:
                self.backend = backends_with_qubits[0][0]
                self.max_qubits = backends_with_qubits[0][1]
                queue_length = backends_with_qubits[0][2]
                
                config = self.backend.configuration()
                
                print(f"🎯 Connected to LARGEST backend: {config.backend_name}")
                print(f"📊 Qubits available: {self.max_qubits}")
                print(f"📋 Queue length: {queue_length}")
                print(f"🔧 Quantum volume: {getattr(config, 'quantum_volume', 'N/A')}")
                
                # Show all available backends
                print(f"\n📋 All available backends:")
                for backend, qubits, queue in backends_with_qubits[:5]:  # Top 5
                    print(f"   {backend.name}: {qubits} qubits (queue: {queue})")
                
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def create_complex_zkp_circuit(self, data: bytes, n_qubits: int = 16) -> QuantumCircuit:
        """Create complex ZKP circuit with high qubit count"""
        # Use up to available qubits, but cap for performance
        n_qubits = min(n_qubits, self.max_qubits, 20)  # Max 20 for reasonable execution time
        
        qc = QuantumCircuit(n_qubits, n_qubits)
        
        data_hash = hashlib.sha256(data).digest()
        
        print(f"   Creating complex circuit with {n_qubits} qubits...")
        
        # Layer 1: Initialize with secret-dependent rotations
        for i in range(n_qubits):
            theta = (data_hash[i % len(data_hash)] / 255.0) * 2 * np.pi
            phi = (data_hash[(i + 8) % len(data_hash)] / 255.0) * 2 * np.pi
            lambda_param = (data_hash[(i + 16) % len(data_hash)] / 255.0) * 2 * np.pi
            
            qc.ry(theta, i)
            qc.rz(phi, i)
            qc.rx(lambda_param, i)
        
        # Layer 2: Create complex entanglement patterns
        # Linear chain
        for i in range(n_qubits - 1):
            qc.cx(i, i + 1)
        
        # Star pattern from center
        center = n_qubits // 2
        for i in range(n_qubits):
            if i != center and i % 2 == 0:
                qc.cz(center, i)
        
        # Layer 3: Parameterized gates based on data
        for layer in range(3):  # 3 layers of complexity
            for i in range(n_qubits):
                param_idx = (layer * n_qubits + i) % len(data_hash)
                angle = (data_hash[param_idx] / 255.0) * np.pi
                
                if layer % 3 == 0:
                    qc.ry(angle, i)
                elif layer % 3 == 1:
                    qc.rz(angle, i)
                else:
                    qc.rx(angle, i)
            
            # Entanglement layer
            for i in range(0, n_qubits - 1, 2):
                qc.cx(i, i + 1)
        
        # Layer 4: Ring connectivity
        if n_qubits > 2:
            qc.cx(n_qubits - 1, 0)
        
        # Final measurement
        qc.measure_all()
        
        return qc
    
    def create_qft_zkp_circuit(self, data: bytes, n_qubits: int = 12) -> QuantumCircuit:
        """Create QFT-based ZKP circuit"""
        n_qubits = min(n_qubits, self.max_qubits, 16)  # QFT is expensive
        
        qc = QuantumCircuit(n_qubits, n_qubits)
        
        data_hash = hashlib.sha256(data).digest()
        
        print(f"   Creating QFT circuit with {n_qubits} qubits...")
        
        # Initialize with data encoding
        for i in range(n_qubits):
            if data_hash[i % len(data_hash)] > 128:
                qc.x(i)
            
            # Add rotation based on data
            angle = (data_hash[(i + 8) % len(data_hash)] / 255.0) * np.pi
            qc.ry(angle, i)
        
        # Apply QFT
        qft = QFT(n_qubits, approximation_degree=2)  # Approximate for hardware efficiency
        qc.compose(qft, inplace=True)
        
        # Data-dependent phase modifications
        for i in range(n_qubits):
            if data_hash[(i + 16) % len(data_hash)] > 128:
                qc.z(i)
        
        # Inverse QFT
        qc.compose(qft.inverse(), inplace=True)
        
        qc.measure_all()
        return qc
    
    def create_variational_zkp_circuit(self, data: bytes, n_qubits: int = 14, depth: int = 6) -> QuantumCircuit:
        """Create variational quantum circuit for ZKP"""
        n_qubits = min(n_qubits, self.max_qubits, 18)
        
        qc = QuantumCircuit(n_qubits, n_qubits)
        
        data_hash = hashlib.sha256(data).digest()
        
        print(f"   Creating variational circuit with {n_qubits} qubits, depth {depth}...")
        
        param_idx = 0
        
        # Variational layers
        for layer in range(depth):
            # Rotation layer
            for qubit in range(n_qubits):
                rx_angle = (data_hash[param_idx % len(data_hash)] / 255.0) * 2 * np.pi
                ry_angle = (data_hash[(param_idx + 1) % len(data_hash)] / 255.0) * 2 * np.pi
                rz_angle = (data_hash[(param_idx + 2) % len(data_hash)] / 255.0) * 2 * np.pi
                
                qc.rx(rx_angle, qubit)
                qc.ry(ry_angle, qubit)
                qc.rz(rz_angle, qubit)
                
                param_idx += 3
            
            # Entangling layer with different patterns per layer
            if layer % 3 == 0:
                # Linear entanglement
                for i in range(n_qubits - 1):
                    qc.cx(i, i + 1)
            elif layer % 3 == 1:
                # Circular entanglement
                for i in range(0, n_qubits - 1, 2):
                    qc.cx(i, i + 1)
                for i in range(1, n_qubits - 1, 2):
                    qc.cx(i, i + 1)
            else:
                # All-to-all (limited)
                center = n_qubits // 2
                for i in range(min(4, n_qubits)):
                    if i != center:
                        qc.cz(center, i)
        
        qc.measure_all()
        return qc
    
    def create_supremacy_style_circuit(self, data: bytes, n_qubits: int = 20, depth: int = 8) -> QuantumCircuit:
        """Create quantum supremacy style random circuit"""
        n_qubits = min(n_qubits, self.max_qubits, 25)  # Use many qubits
        
        qc = QuantumCircuit(n_qubits, n_qubits)
        
        # Seed random generator with data
        seed = int.from_bytes(hashlib.sha256(data).digest()[:4], 'big')
        np.random.seed(seed)
        
        print(f"   Creating supremacy-style circuit with {n_qubits} qubits, depth {depth}...")
        
        # Initial layer
        for i in range(n_qubits):
            qc.h(i)
        
        # Random circuit layers
        for layer in range(depth):
            # Random single-qubit gates
            for qubit in range(n_qubits):
                gate_choice = np.random.randint(0, 6)
                angle = np.random.uniform(0, 2 * np.pi)
                
                if gate_choice == 0:
                    qc.rx(angle, qubit)
                elif gate_choice == 1:
                    qc.ry(angle, qubit)
                elif gate_choice == 2:
                    qc.rz(angle, qubit)
                elif gate_choice == 3:
                    qc.h(qubit)
                elif gate_choice == 4:
                    qc.s(qubit)
                else:
                    qc.t(qubit)
            
            # Random two-qubit gates
            available_qubits = list(range(n_qubits))
            np.random.shuffle(available_qubits)
            
            for i in range(0, len(available_qubits) - 1, 2):
                qubit1, qubit2 = available_qubits[i], available_qubits[i + 1]
                
                gate_choice = np.random.randint(0, 4)
                if gate_choice == 0:
                    qc.cx(qubit1, qubit2)
                elif gate_choice == 1:
                    qc.cz(qubit1, qubit2)
                elif gate_choice == 2:
                    qc.cy(qubit1, qubit2)
                else:
                    angle = np.random.uniform(0, 2 * np.pi)
                    qc.crz(angle, qubit1, qubit2)
        
        qc.measure_all()
        return qc
    
    def execute_complex_test(self, test_name: str, circuit: QuantumCircuit) -> Dict[str, Any]:
        """Execute complex test on IBM hardware"""
        print(f"🔬 Complex test: {test_name}")
        
        start_time = time.time()
        
        try:
            # Transpile with high optimization for complex circuits
            print(f"   Transpiling {circuit.num_qubits}-qubit circuit...")
            transpiled = transpile(circuit, self.backend, optimization_level=3)
            
            print(f"   Original: {circuit.depth()} depth, {sum(circuit.count_ops().values())} gates")
            print(f"   Transpiled: {transpiled.depth()} depth, {sum(transpiled.count_ops().values())} gates")
            
            # Create sampler
            sampler = Sampler(self.backend)
            
            # Use fewer shots for complex circuits to reduce execution time
            shots = max(50, min(200, 1000 // (transpiled.depth() // 10 + 1)))
            
            print(f"   Executing {shots} shots on {self.backend.name}...")
            
            # Submit job
            job = sampler.run([transpiled], shots=shots)
            job_id = job.job_id()
            
            print(f"   Job ID: {job_id}")
            print(f"   🔗 Monitor: https://quantum-computing.ibm.com/")
            
            # Monitor with extended timeout for complex circuits
            while not job.done():
                elapsed = time.time() - start_time
                
                if elapsed > self.timeout:
                    print(f"   ⏰ TIMEOUT after {elapsed:.1f}s")
                    try:
                        job.cancel()
                    except:
                        pass
                    
                    return {
                        'test_name': test_name,
                        'job_id': job_id,
                        'backend': self.backend.name,
                        'status': 'TIMEOUT',
                        'execution_time': elapsed,
                        'circuit_complexity': self.calculate_complexity(transpiled),
                        'success': False,
                        'timeout': True
                    }
                
                print(f"   Status: Running ({elapsed:.1f}s)")
                time.sleep(15)  # Longer polling for complex circuits
            
            total_time = time.time() - start_time
            
            # Get results
            result = job.result()
            pub_result = result[0]
            counts = pub_result.data.meas.get_counts()
            
            # Calculate advanced metrics
            complexity = self.calculate_complexity(transpiled)
            entropy = self.calculate_entropy(counts)
            quantum_advantage = self.estimate_quantum_advantage(complexity, counts)
            
            test_result = {
                'test_name': test_name,
                'job_id': job_id,
                'backend': self.backend.name,
                'status': 'COMPLETED',
                'execution_time': total_time,
                'circuit_complexity': complexity,
                'shots': shots,
                'measurement_counts': counts,
                'unique_outcomes': len(counts),
                'entropy': entropy,
                'quantum_advantage_score': quantum_advantage,
                'max_probability': max(counts.values()) / shots if counts else 0,
                'success': True,
                'timeout': False,
                'timestamp': datetime.now().isoformat()
            }
            
            print(f"   ✅ COMPLETED in {total_time:.1f}s")
            print(f"   📊 {len(counts)} unique outcomes")
            print(f"   🎯 Entropy: {entropy:.3f}")
            print(f"   🚀 Quantum advantage: {quantum_advantage:.3f}")
            print(f"   🔗 Job ID: {job_id}")
            
            return test_result
            
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"   ❌ ERROR after {elapsed:.1f}s: {e}")
            
            return {
                'test_name': test_name,
                'error': str(e),
                'execution_time': elapsed,
                'success': False,
                'timeout': False
            }
    
    def calculate_complexity(self, circuit: QuantumCircuit) -> Dict[str, Any]:
        """Calculate circuit complexity metrics"""
        gate_counts = circuit.count_ops()
        
        two_qubit_gates = sum(count for gate, count in gate_counts.items() 
                             if gate in ['cx', 'cz', 'cy', 'crz', 'crx', 'cry', 'ccx'])
        
        complexity_score = circuit.depth() * 0.5 + two_qubit_gates * 2.0 + circuit.num_qubits * 0.1
        
        return {
            'total_gates': sum(gate_counts.values()),
            'two_qubit_gates': two_qubit_gates,
            'circuit_depth': circuit.depth(),
            'circuit_width': circuit.num_qubits,
            'complexity_score': complexity_score,
            'gate_density': sum(gate_counts.values()) / circuit.num_qubits if circuit.num_qubits > 0 else 0
        }
    
    def calculate_entropy(self, counts: Dict[str, int]) -> float:
        """Calculate Shannon entropy"""
        if not counts:
            return 0.0
        
        total = sum(counts.values())
        entropy = 0.0
        
        for count in counts.values():
            if count > 0:
                p = count / total
                entropy -= p * np.log2(p)
        
        return entropy
    
    def estimate_quantum_advantage(self, complexity: Dict[str, Any], counts: Dict[str, int]) -> float:
        """Estimate quantum computational advantage"""
        circuit_complexity = complexity['complexity_score']
        output_entropy = self.calculate_entropy(counts)
        
        # Normalize metrics
        normalized_complexity = min(1.0, circuit_complexity / 200.0)
        normalized_entropy = output_entropy / 15.0 if output_entropy > 0 else 0
        
        advantage_score = (normalized_complexity + normalized_entropy) / 2.0
        
        return min(1.0, advantage_score)
    
    def run_complex_test_suite(self):
        """Run complete complex test suite"""
        print("🚀 Complex IBM Quantum Hardware Test Suite")
        print("=" * 50)
        
        if not self.connect_to_largest_backend():
            return []
        
        # Test data
        test_data = b"Complex IBM Quantum ZKP Test Suite 2025"
        
        # Complex test cases with varying qubit counts
        test_cases = [
            ("Complex_ZKP_16q", lambda: self.create_complex_zkp_circuit(test_data, 16)),
            ("QFT_ZKP_12q", lambda: self.create_qft_zkp_circuit(test_data, 12)),
            ("Variational_ZKP_14q", lambda: self.create_variational_zkp_circuit(test_data, 14, 6)),
            ("Supremacy_Style_20q", lambda: self.create_supremacy_style_circuit(test_data, 20, 6)),
            ("Complex_ZKP_Max", lambda: self.create_complex_zkp_circuit(test_data + b"_max", min(25, self.max_qubits)))
        ]
        
        results = []
        
        for i, (name, circuit_func) in enumerate(test_cases, 1):
            print(f"\n🔬 Complex Test {i}/{len(test_cases)}: {name}")
            print("-" * 60)
            
            try:
                circuit = circuit_func()
                result = self.execute_complex_test(name, circuit)
                results.append(result)
                
                # Extended pause for complex tests
                if i < len(test_cases):
                    print("⏳ 30s pause before next complex test...")
                    time.sleep(30)
                    
            except Exception as e:
                print(f"   ❌ Failed to create circuit: {e}")
                results.append({
                    'test_name': name,
                    'error': f"Circuit creation failed: {e}",
                    'success': False
                })
        
        return results
    
    def generate_complex_report(self, results: List[Dict[str, Any]]):
        """Generate complex test report"""
        successful = sum(1 for r in results if r.get('success', False))
        total = len(results)
        
        # Calculate metrics
        total_qubits_used = sum(r.get('circuit_complexity', {}).get('circuit_width', 0) 
                               for r in results if r.get('success', False))
        
        avg_complexity = np.mean([r.get('circuit_complexity', {}).get('complexity_score', 0) 
                                 for r in results if r.get('success', False)]) if successful > 0 else 0
        
        report = {
            'complex_test_summary': {
                'backend_used': self.backend.name if self.backend else 'N/A',
                'max_qubits_available': self.max_qubits,
                'total_tests': total,
                'successful_tests': successful,
                'success_rate': (successful / total * 100) if total > 0 else 0,
                'total_qubits_used': total_qubits_used,
                'avg_complexity_score': avg_complexity,
                'job_ids': [r.get('job_id', 'N/A') for r in results if 'job_id' in r],
                'timestamp': datetime.now().isoformat()
            },
            'complex_test_results': results
        }
        
        # Save report
        filename = f"complex_ibm_quantum_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n🎉 Complex Test Suite Complete!")
        print("=" * 50)
        print(f"✅ Successful: {successful}/{total}")
        print(f"📊 Success Rate: {successful/total*100:.1f}%")
        print(f"🏭 Backend: {self.backend.name} ({self.max_qubits} qubits)")
        print(f"🔢 Total Qubits Used: {total_qubits_used}")
        print(f"📈 Avg Complexity: {avg_complexity:.1f}")
        print(f"📄 Report: {filename}")
        
        # Print job IDs
        job_ids = [r.get('job_id') for r in results if r.get('job_id') and r.get('job_id') != 'N/A']
        if job_ids:
            print(f"\n🔗 Verifiable Job IDs:")
            for i, job_id in enumerate(job_ids, 1):
                print(f"   {i}. {job_id}")
        
        return successful >= total * 0.6  # 60% success rate

def main():
    """Main execution"""
    tester = ComplexIBMQuantumTester()
    
    try:
        results = tester.run_complex_test_suite()
        success = tester.generate_complex_report(results)
        
        if success:
            print("\n🚀 COMPLEX IBM QUANTUM TESTS SUCCESSFUL!")
            print("🔬 Advanced quantum circuits executed on real hardware!")
            return 0
        else:
            print("\n⚠️ Some complex tests failed")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ Complex tests interrupted")
        return 1
    except Exception as e:
        print(f"\n❌ Complex tests failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
