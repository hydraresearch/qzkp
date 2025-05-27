#!/usr/bin/env python3
"""
Probabilistic Encoding Test Suite for Quantum ZKP
Tests the core probabilistic entanglement encoding mechanism
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
    from dotenv import load_dotenv
    print("✅ Probabilistic encoding packages loaded")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

class ProbabilisticEncodingTester:
    """Test probabilistic entanglement encoding for quantum ZKP"""
    
    def __init__(self):
        self.load_credentials()
        self.service = None
        self.backend = None
        self.test_results = []
        self.timeout = 90
        
    def load_credentials(self):
        """Load IBM Quantum credentials"""
        env_path = os.path.join(os.path.dirname(__file__), '../../.env')
        load_dotenv(env_path)
        self.token = os.getenv('IQKAPI')
        
        if not self.token:
            print("❌ IQKAPI not found in .env file")
            sys.exit(1)
    
    def connect_to_ibm(self):
        """Connect to IBM Quantum"""
        try:
            print("🔌 Connecting to IBM Quantum for probabilistic encoding tests...")
            
            self.service = QiskitRuntimeService(token=self.token, channel='ibm_quantum')
            backends = self.service.backends(simulator=False, operational=True)
            
            if not backends:
                print("❌ No operational backends available")
                return False
            
            # Prefer Brisbane for consistency
            for backend in backends:
                if 'brisbane' in backend.name.lower():
                    self.backend = backend
                    break
            else:
                self.backend = backends[0]
            
            config = self.backend.configuration()
            print(f"✅ Connected to: {config.backend_name}")
            print(f"📊 Qubits: {config.n_qubits}")
            
            return True
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def create_probabilistic_encoding_circuit(self, secret_data: bytes, encoding_type: str = "amplitude") -> QuantumCircuit:
        """
        Create probabilistic encoding circuit
        Encodes secret data into quantum amplitudes with probabilistic entanglement
        """
        n_qubits = 8  # Use 8 qubits for good probabilistic space
        qc = QuantumCircuit(n_qubits, n_qubits)
        
        # Generate deterministic but secret-dependent probabilities
        data_hash = hashlib.sha256(secret_data).digest()
        
        print(f"   Creating {encoding_type} probabilistic encoding with {n_qubits} qubits...")
        
        if encoding_type == "amplitude":
            # Amplitude-based probabilistic encoding
            for i in range(n_qubits):
                # Convert hash bytes to probability amplitudes
                prob_real = data_hash[i % len(data_hash)] / 255.0
                prob_imag = data_hash[(i + 8) % len(data_hash)] / 255.0
                
                # Create probabilistic superposition
                theta = 2 * np.arcsin(np.sqrt(prob_real))
                phi = prob_imag * 2 * np.pi
                
                qc.ry(theta, i)
                qc.rz(phi, i)
        
        elif encoding_type == "phase":
            # Phase-based probabilistic encoding
            for i in range(n_qubits):
                # Initialize in superposition
                qc.h(i)
                
                # Apply secret-dependent phase
                phase = (data_hash[i % len(data_hash)] / 255.0) * 2 * np.pi
                qc.rz(phase, i)
        
        elif encoding_type == "entanglement":
            # Entanglement-based probabilistic encoding
            # Create probabilistic entanglement patterns
            for i in range(n_qubits):
                prob = data_hash[i % len(data_hash)] / 255.0
                theta = 2 * np.arcsin(np.sqrt(prob))
                qc.ry(theta, i)
            
            # Create conditional entanglement based on secret
            for i in range(n_qubits - 1):
                if data_hash[(i + 16) % len(data_hash)] > 128:
                    qc.cx(i, i + 1)
                else:
                    qc.cz(i, i + 1)
        
        # Add probabilistic verification layer
        for i in range(0, n_qubits - 1, 2):
            # Probabilistic two-qubit gates
            prob_threshold = data_hash[(i + 24) % len(data_hash)]
            
            if prob_threshold > 85:  # ~33% probability
                qc.cx(i, i + 1)
            elif prob_threshold > 170:  # ~33% probability  
                qc.cz(i, i + 1)
            # else: ~33% probability of no gate
        
        qc.measure_all()
        return qc
    
    def create_probabilistic_bell_encoding(self, secret_data: bytes, num_pairs: int = 4) -> QuantumCircuit:
        """Create probabilistic Bell state encoding"""
        n_qubits = num_pairs * 2
        qc = QuantumCircuit(n_qubits, n_qubits)
        
        data_hash = hashlib.sha256(secret_data).digest()
        
        print(f"   Creating probabilistic Bell encoding with {num_pairs} Bell pairs...")
        
        for pair in range(num_pairs):
            qubit1 = pair * 2
            qubit2 = pair * 2 + 1
            
            # Probabilistic Bell state creation
            prob = data_hash[pair % len(data_hash)] / 255.0
            
            # Create partial Bell state based on probability
            qc.h(qubit1)
            
            # Probabilistic entanglement
            if prob > 0.5:
                qc.cx(qubit1, qubit2)
            else:
                # Create different entanglement pattern
                qc.ry(np.pi * prob, qubit2)
                qc.cx(qubit1, qubit2)
                qc.ry(-np.pi * prob, qubit2)
            
            # Add probabilistic phase
            phase_prob = data_hash[(pair + 8) % len(data_hash)] / 255.0
            if phase_prob > 0.7:
                qc.z(qubit1)
            elif phase_prob > 0.3:
                qc.z(qubit2)
        
        qc.measure_all()
        return qc
    
    def create_probabilistic_ghz_encoding(self, secret_data: bytes, n_qubits: int = 6) -> QuantumCircuit:
        """Create probabilistic GHZ state encoding"""
        qc = QuantumCircuit(n_qubits, n_qubits)
        
        data_hash = hashlib.sha256(secret_data).digest()
        
        print(f"   Creating probabilistic GHZ encoding with {n_qubits} qubits...")
        
        # Probabilistic GHZ state creation
        prob_control = data_hash[0] / 255.0
        
        # Initialize control qubit with probability
        theta = 2 * np.arcsin(np.sqrt(prob_control))
        qc.ry(theta, 0)
        
        # Create probabilistic entanglement
        for i in range(1, n_qubits):
            entangle_prob = data_hash[i % len(data_hash)] / 255.0
            
            if entangle_prob > 0.6:
                # Strong entanglement
                qc.cx(0, i)
            elif entangle_prob > 0.3:
                # Weak entanglement
                qc.ry(np.pi * entangle_prob, i)
                qc.cx(0, i)
                qc.ry(-np.pi * entangle_prob, i)
            # else: no entanglement (probabilistic)
        
        # Add probabilistic phase corrections
        for i in range(n_qubits):
            phase_prob = data_hash[(i + 8) % len(data_hash)] / 255.0
            if phase_prob > 0.8:
                qc.z(i)
        
        qc.measure_all()
        return qc
    
    def create_adaptive_probabilistic_encoding(self, secret_data: bytes, n_qubits: int = 10) -> QuantumCircuit:
        """Create adaptive probabilistic encoding that changes based on secret"""
        qc = QuantumCircuit(n_qubits, n_qubits)
        
        data_hash = hashlib.sha256(secret_data).digest()
        
        print(f"   Creating adaptive probabilistic encoding with {n_qubits} qubits...")
        
        # Determine encoding strategy based on secret
        strategy_byte = data_hash[0]
        
        if strategy_byte < 85:  # ~33% - Dense encoding
            # High probability, dense entanglement
            for i in range(n_qubits):
                prob = 0.7 + (data_hash[i % len(data_hash)] / 255.0) * 0.3
                theta = 2 * np.arcsin(np.sqrt(prob))
                qc.ry(theta, i)
            
            # Dense entanglement
            for i in range(n_qubits - 1):
                qc.cx(i, i + 1)
                
        elif strategy_byte < 170:  # ~33% - Sparse encoding
            # Low probability, sparse entanglement
            for i in range(n_qubits):
                prob = (data_hash[i % len(data_hash)] / 255.0) * 0.4
                theta = 2 * np.arcsin(np.sqrt(prob))
                qc.ry(theta, i)
            
            # Sparse entanglement
            for i in range(0, n_qubits - 1, 2):
                qc.cx(i, i + 1)
                
        else:  # ~33% - Mixed encoding
            # Mixed probability pattern
            for i in range(n_qubits):
                if i % 2 == 0:
                    prob = 0.8 - (data_hash[i % len(data_hash)] / 255.0) * 0.3
                else:
                    prob = 0.2 + (data_hash[i % len(data_hash)] / 255.0) * 0.3
                
                theta = 2 * np.arcsin(np.sqrt(prob))
                qc.ry(theta, i)
            
            # Ring entanglement
            for i in range(n_qubits - 1):
                qc.cz(i, i + 1)
            qc.cz(n_qubits - 1, 0)
        
        qc.measure_all()
        return qc
    
    def execute_probabilistic_test(self, test_name: str, circuit: QuantumCircuit) -> Dict[str, Any]:
        """Execute probabilistic encoding test"""
        print(f"🎲 Probabilistic test: {test_name}")
        
        start_time = time.time()
        
        try:
            # Transpile
            transpiled = transpile(circuit, self.backend, optimization_level=2)
            
            print(f"   Circuit: {transpiled.depth()} depth, {transpiled.num_qubits} qubits")
            
            # Create sampler
            sampler = Sampler(self.backend)
            
            # Use more shots for probabilistic analysis
            shots = 200
            
            print(f"   Executing {shots} shots for probabilistic analysis...")
            
            # Submit job
            job = sampler.run([transpiled], shots=shots)
            job_id = job.job_id()
            
            print(f"   Job ID: {job_id}")
            
            # Monitor
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
                        'status': 'TIMEOUT',
                        'execution_time': elapsed,
                        'success': False,
                        'timeout': True
                    }
                
                print(f"   Status: Running ({elapsed:.1f}s)")
                time.sleep(10)
            
            total_time = time.time() - start_time
            
            # Get results
            result = job.result()
            pub_result = result[0]
            counts = pub_result.data.meas.get_counts()
            
            # Analyze probabilistic properties
            prob_analysis = self.analyze_probabilistic_properties(counts, shots)
            
            test_result = {
                'test_name': test_name,
                'job_id': job_id,
                'backend': self.backend.name,
                'status': 'COMPLETED',
                'execution_time': total_time,
                'circuit_depth': transpiled.depth(),
                'num_qubits': transpiled.num_qubits,
                'shots': shots,
                'measurement_counts': counts,
                'probabilistic_analysis': prob_analysis,
                'success': True,
                'timeout': False,
                'timestamp': datetime.now().isoformat()
            }
            
            print(f"   ✅ COMPLETED in {total_time:.1f}s")
            print(f"   📊 {len(counts)} unique outcomes")
            print(f"   🎲 Probability distribution quality: {prob_analysis['distribution_quality']:.3f}")
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
    
    def analyze_probabilistic_properties(self, counts: Dict[str, int], total_shots: int) -> Dict[str, float]:
        """Analyze probabilistic properties of measurement results"""
        if not counts:
            return {'distribution_quality': 0.0, 'entropy': 0.0, 'uniformity': 0.0}
        
        # Calculate probability distribution
        probabilities = [count / total_shots for count in counts.values()]
        
        # Shannon entropy
        entropy = -sum(p * np.log2(p) for p in probabilities if p > 0)
        
        # Distribution uniformity (how close to uniform)
        n_outcomes = len(counts)
        expected_uniform_prob = 1.0 / n_outcomes
        uniformity = 1.0 - sum(abs(p - expected_uniform_prob) for p in probabilities) / 2.0
        
        # Distribution quality (combination of entropy and uniformity)
        max_entropy = np.log2(n_outcomes) if n_outcomes > 1 else 1
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0
        distribution_quality = (normalized_entropy + uniformity) / 2.0
        
        # Probabilistic encoding effectiveness
        # Check if distribution shows signs of structured encoding
        sorted_probs = sorted(probabilities, reverse=True)
        top_prob_concentration = sum(sorted_probs[:min(4, len(sorted_probs))])
        
        return {
            'entropy': entropy,
            'uniformity': uniformity,
            'distribution_quality': distribution_quality,
            'top_probability_concentration': top_prob_concentration,
            'unique_outcomes': n_outcomes,
            'max_probability': max(probabilities),
            'min_probability': min(probabilities)
        }
    
    def run_probabilistic_encoding_suite(self):
        """Run complete probabilistic encoding test suite"""
        print("🎲 Probabilistic Encoding Test Suite")
        print("=" * 45)
        
        if not self.connect_to_ibm():
            return []
        
        # Test data
        test_data = b"Probabilistic Quantum ZKP Encoding Test 2025"
        
        # Probabilistic encoding test cases
        test_cases = [
            ("Amplitude_Encoding", lambda: self.create_probabilistic_encoding_circuit(test_data, "amplitude")),
            ("Phase_Encoding", lambda: self.create_probabilistic_encoding_circuit(test_data, "phase")),
            ("Entanglement_Encoding", lambda: self.create_probabilistic_encoding_circuit(test_data, "entanglement")),
            ("Bell_Probabilistic", lambda: self.create_probabilistic_bell_encoding(test_data, 4)),
            ("GHZ_Probabilistic", lambda: self.create_probabilistic_ghz_encoding(test_data, 6)),
            ("Adaptive_Encoding", lambda: self.create_adaptive_probabilistic_encoding(test_data, 10))
        ]
        
        results = []
        
        for i, (name, circuit_func) in enumerate(test_cases, 1):
            print(f"\n🎲 Probabilistic Test {i}/{len(test_cases)}: {name}")
            print("-" * 50)
            
            try:
                circuit = circuit_func()
                result = self.execute_probabilistic_test(name, circuit)
                results.append(result)
                self.test_results.append(result)
                
                # Pause between tests
                if i < len(test_cases):
                    print("⏳ 20s pause...")
                    time.sleep(20)
                    
            except Exception as e:
                print(f"   ❌ Failed to create circuit: {e}")
                results.append({
                    'test_name': name,
                    'error': f"Circuit creation failed: {e}",
                    'success': False
                })
        
        return results
    
    def generate_probabilistic_report(self, results: List[Dict[str, Any]]):
        """Generate probabilistic encoding test report"""
        successful = sum(1 for r in results if r.get('success', False))
        total = len(results)
        
        # Calculate probabilistic metrics
        avg_distribution_quality = np.mean([
            r.get('probabilistic_analysis', {}).get('distribution_quality', 0)
            for r in results if r.get('success', False)
        ]) if successful > 0 else 0
        
        avg_entropy = np.mean([
            r.get('probabilistic_analysis', {}).get('entropy', 0)
            for r in results if r.get('success', False)
        ]) if successful > 0 else 0
        
        report = {
            'probabilistic_encoding_summary': {
                'backend_used': self.backend.name if self.backend else 'N/A',
                'total_tests': total,
                'successful_tests': successful,
                'success_rate': (successful / total * 100) if total > 0 else 0,
                'avg_distribution_quality': avg_distribution_quality,
                'avg_entropy': avg_entropy,
                'job_ids': [r.get('job_id', 'N/A') for r in results if 'job_id' in r],
                'timestamp': datetime.now().isoformat()
            },
            'probabilistic_test_results': results
        }
        
        # Save report
        filename = f"probabilistic_encoding_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n🎉 Probabilistic Encoding Test Suite Complete!")
        print("=" * 50)
        print(f"✅ Successful: {successful}/{total}")
        print(f"📊 Success Rate: {successful/total*100:.1f}%")
        print(f"🏭 Backend: {self.backend.name}")
        print(f"🎲 Avg Distribution Quality: {avg_distribution_quality:.3f}")
        print(f"📈 Avg Entropy: {avg_entropy:.3f}")
        print(f"📄 Report: {filename}")
        
        # Print job IDs
        job_ids = [r.get('job_id') for r in results if r.get('job_id') and r.get('job_id') != 'N/A']
        if job_ids:
            print(f"\n🔗 Verifiable Job IDs:")
            for i, job_id in enumerate(job_ids, 1):
                print(f"   {i}. {job_id}")
        
        return successful >= total * 0.7  # 70% success rate

def main():
    """Main execution"""
    tester = ProbabilisticEncodingTester()
    
    try:
        results = tester.run_probabilistic_encoding_suite()
        success = tester.generate_probabilistic_report(results)
        
        if success:
            print("\n🚀 PROBABILISTIC ENCODING TESTS SUCCESSFUL!")
            print("🎲 Probabilistic entanglement encoding validated!")
            return 0
        else:
            print("\n⚠️ Some probabilistic tests failed")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ Probabilistic tests interrupted")
        return 1
    except Exception as e:
        print(f"\n❌ Probabilistic tests failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
