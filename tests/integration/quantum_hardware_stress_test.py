#!/usr/bin/env python3
"""
Quantum Hardware Stress Test Suite
Pushes IBM Quantum hardware to limits with complex ZKP circuits
"""

import os
import sys
import json
import time
import hashlib
import numpy as np
from datetime import datetime
from typing import List, Dict, Any, Tuple
import concurrent.futures

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

try:
    from qiskit import QuantumCircuit, transpile, execute
    from qiskit.providers.ibmq import IBMQ
    from qiskit.providers import JobStatus
    from qiskit.quantum_info import random_unitary, Statevector
    from qiskit.circuit.library import QFT, GroverOperator
    from dotenv import load_dotenv
    print("✅ Quantum stress test packages loaded")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

class QuantumHardwareStressTest:
    """Comprehensive quantum hardware stress testing for ZKP systems"""
    
    def __init__(self):
        self.load_credentials()
        self.provider = None
        self.backend = None
        self.stress_results = []
        self.max_qubits = 0
        self.backend_properties = {}
        
    def load_credentials(self):
        """Load IBM Quantum credentials"""
        env_path = os.path.join(os.path.dirname(__file__), '../../.env')
        load_dotenv(env_path)
        self.token = os.getenv('IBM_QUANTUM_TOKEN')
        
    def connect_to_ibm(self):
        """Connect to IBM Quantum and analyze backend capabilities"""
        try:
            IBMQ.save_account(self.token, overwrite=True)
            IBMQ.load_account()
            self.provider = IBMQ.get_provider(hub='ibm-q')
            
            # Select the most capable backend
            backends = self.provider.backends(simulator=False, operational=True)
            best_backend = max(backends, key=lambda x: x.configuration().n_qubits)
            
            self.backend = best_backend
            config = self.backend.configuration()
            self.max_qubits = config.n_qubits
            
            # Get backend properties for stress testing
            try:
                properties = self.backend.properties()
                self.backend_properties = {
                    'gate_errors': self.extract_gate_errors(properties),
                    'readout_errors': self.extract_readout_errors(properties),
                    'coherence_times': self.extract_coherence_times(properties)
                }
            except:
                self.backend_properties = {}
            
            print(f"✅ Connected to {config.backend_name}")
            print(f"📊 Backend capabilities:")
            print(f"   Qubits: {self.max_qubits}")
            print(f"   Max shots: {config.max_shots}")
            print(f"   Quantum volume: {getattr(config, 'quantum_volume', 'N/A')}")
            
            return True
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def extract_gate_errors(self, properties) -> Dict[str, float]:
        """Extract gate error rates from backend properties"""
        gate_errors = {}
        try:
            for gate in properties.gates:
                gate_errors[gate.gate] = gate.parameters[0].value
        except:
            pass
        return gate_errors
    
    def extract_readout_errors(self, properties) -> List[float]:
        """Extract readout error rates"""
        try:
            return [qubit.readout_error for qubit in properties.qubits]
        except:
            return []
    
    def extract_coherence_times(self, properties) -> Dict[str, List[float]]:
        """Extract T1 and T2 coherence times"""
        try:
            t1_times = []
            t2_times = []
            for qubit in properties.qubits:
                for param in qubit:
                    if param.name == 'T1':
                        t1_times.append(param.value)
                    elif param.name == 'T2':
                        t2_times.append(param.value)
            return {'T1': t1_times, 'T2': t2_times}
        except:
            return {'T1': [], 'T2': []}
    
    def create_maximum_depth_circuit(self, secret_data: bytes, target_depth: int = 100) -> QuantumCircuit:
        """Create maximum depth circuit for stress testing"""
        n_qubits = min(8, self.max_qubits)  # Use reasonable number of qubits
        qc = QuantumCircuit(n_qubits, n_qubits)
        
        data_hash = hashlib.sha256(secret_data).digest()
        
        # Build deep circuit layer by layer
        current_depth = 0
        layer = 0
        
        while current_depth < target_depth:
            # Rotation layer
            for qubit in range(n_qubits):
                if current_depth >= target_depth:
                    break
                angle = (data_hash[(layer * n_qubits + qubit) % len(data_hash)] / 255.0) * 2 * np.pi
                qc.ry(angle, qubit)
                current_depth += 1
            
            # Entanglement layer
            for qubit in range(n_qubits - 1):
                if current_depth >= target_depth:
                    break
                qc.cx(qubit, qubit + 1)
                current_depth += 1
            
            layer += 1
        
        qc.measure_all()
        return qc
    
    def create_maximum_width_circuit(self, secret_data: bytes) -> QuantumCircuit:
        """Create maximum width circuit using all available qubits"""
        n_qubits = self.max_qubits
        qc = QuantumCircuit(n_qubits, n_qubits)
        
        data_hash = hashlib.sha256(secret_data).digest()
        
        # Initialize all qubits
        for qubit in range(n_qubits):
            angle = (data_hash[qubit % len(data_hash)] / 255.0) * 2 * np.pi
            qc.ry(angle, qubit)
        
        # Create maximum entanglement
        # Linear chain
        for qubit in range(n_qubits - 1):
            qc.cx(qubit, qubit + 1)
        
        # Star pattern from center
        center = n_qubits // 2
        for qubit in range(n_qubits):
            if qubit != center:
                qc.cz(center, qubit)
        
        # Ring connectivity
        qc.cx(n_qubits - 1, 0)
        
        qc.measure_all()
        return qc
    
    def create_high_gate_count_circuit(self, secret_data: bytes, target_gates: int = 1000) -> QuantumCircuit:
        """Create circuit with maximum gate count"""
        n_qubits = min(12, self.max_qubits)
        qc = QuantumCircuit(n_qubits, n_qubits)
        
        data_hash = hashlib.sha256(secret_data).digest()
        gate_count = 0
        param_idx = 0
        
        while gate_count < target_gates:
            # Add various gate types
            for qubit in range(n_qubits):
                if gate_count >= target_gates:
                    break
                
                gate_type = data_hash[param_idx % len(data_hash)] % 6
                angle = (data_hash[(param_idx + 1) % len(data_hash)] / 255.0) * 2 * np.pi
                
                if gate_type == 0:
                    qc.rx(angle, qubit)
                elif gate_type == 1:
                    qc.ry(angle, qubit)
                elif gate_type == 2:
                    qc.rz(angle, qubit)
                elif gate_type == 3:
                    qc.h(qubit)
                elif gate_type == 4:
                    qc.s(qubit)
                else:
                    qc.t(qubit)
                
                gate_count += 1
                param_idx += 2
            
            # Add two-qubit gates
            for i in range(0, n_qubits - 1, 2):
                if gate_count >= target_gates:
                    break
                
                gate_type = data_hash[param_idx % len(data_hash)] % 3
                
                if gate_type == 0:
                    qc.cx(i, i + 1)
                elif gate_type == 1:
                    qc.cz(i, i + 1)
                else:
                    angle = (data_hash[(param_idx + 1) % len(data_hash)] / 255.0) * 2 * np.pi
                    qc.crz(angle, i, i + 1)
                
                gate_count += 1
                param_idx += 2
        
        qc.measure_all()
        return qc
    
    def create_noise_resilient_circuit(self, secret_data: bytes) -> QuantumCircuit:
        """Create circuit designed to test noise resilience"""
        n_qubits = min(10, self.max_qubits)
        qc = QuantumCircuit(n_qubits, n_qubits)
        
        data_hash = hashlib.sha256(secret_data).digest()
        
        # Create highly entangled state susceptible to noise
        # GHZ state preparation
        qc.h(0)
        for i in range(n_qubits - 1):
            qc.cx(i, i + 1)
        
        # Add noise-sensitive operations
        for layer in range(5):
            # Small angle rotations (sensitive to gate errors)
            for qubit in range(n_qubits):
                small_angle = (data_hash[(layer * n_qubits + qubit) % len(data_hash)] / 255.0) * 0.1
                qc.ry(small_angle, qubit)
            
            # Long sequences of gates (sensitive to decoherence)
            for qubit in range(n_qubits):
                qc.h(qubit)
                qc.s(qubit)
                qc.h(qubit)
        
        qc.measure_all()
        return qc
    
    def create_parallel_execution_circuits(self, secret_data: bytes, num_circuits: int = 5) -> List[QuantumCircuit]:
        """Create multiple circuits for parallel execution stress test"""
        circuits = []
        
        for i in range(num_circuits):
            # Vary circuit parameters
            circuit_data = secret_data + i.to_bytes(4, 'big')
            n_qubits = min(6 + i, self.max_qubits)
            
            qc = QuantumCircuit(n_qubits, n_qubits)
            data_hash = hashlib.sha256(circuit_data).digest()
            
            # Create varied circuit structure
            depth = 10 + i * 5
            
            for layer in range(depth):
                for qubit in range(n_qubits):
                    angle = (data_hash[(layer * n_qubits + qubit) % len(data_hash)] / 255.0) * 2 * np.pi
                    qc.ry(angle, qubit)
                
                # Entanglement pattern varies by circuit
                if i % 2 == 0:
                    # Linear chain
                    for qubit in range(n_qubits - 1):
                        qc.cx(qubit, qubit + 1)
                else:
                    # All-to-all (limited)
                    for qubit in range(min(4, n_qubits)):
                        for target in range(qubit + 1, min(qubit + 3, n_qubits)):
                            qc.cz(qubit, target)
            
            qc.measure_all()
            circuits.append(qc)
        
        return circuits
    
    def execute_stress_test(self, test_name: str, circuit: QuantumCircuit, shots: int = 1000) -> Dict[str, Any]:
        """Execute individual stress test"""
        print(f"💪 Stress test: {test_name}")
        
        try:
            # Transpile with maximum optimization
            start_transpile = time.time()
            transpiled_qc = transpile(circuit, self.backend, optimization_level=3)
            transpile_time = time.time() - start_transpile
            
            # Calculate stress metrics
            stress_metrics = self.calculate_stress_metrics(circuit, transpiled_qc)
            
            print(f"   Original: {circuit.depth()} depth, {sum(circuit.count_ops().values())} gates")
            print(f"   Transpiled: {transpiled_qc.depth()} depth, {sum(transpiled_qc.count_ops().values())} gates")
            print(f"   Stress level: {stress_metrics['stress_level']:.2f}")
            
            # Execute with error handling
            start_time = time.time()
            job = execute(transpiled_qc, self.backend, shots=shots)
            
            job_id = job.job_id()
            print(f"   Job ID: {job_id}")
            
            # Monitor with timeout
            timeout = 600  # 10 minutes for stress tests
            start_monitor = time.time()
            
            while job.status() not in [JobStatus.DONE, JobStatus.ERROR, JobStatus.CANCELLED]:
                if time.time() - start_monitor > timeout:
                    print(f"   ⚠️ Stress test timeout after {timeout}s")
                    break
                print(f"   Status: {job.status()}")
                time.sleep(30)
            
            execution_time = time.time() - start_time
            
            result = {
                'test_name': test_name,
                'job_id': job_id,
                'backend': self.backend.name(),
                'status': str(job.status()),
                'execution_time': execution_time,
                'transpile_time': transpile_time,
                'stress_metrics': stress_metrics,
                'shots': shots,
                'timestamp': datetime.now().isoformat(),
                'success': job.status() == JobStatus.DONE
            }
            
            if job.status() == JobStatus.DONE:
                job_result = job.result()
                counts = job_result.get_counts()
                
                # Stress test analysis
                result.update({
                    'measurement_results': counts,
                    'noise_analysis': self.analyze_noise_effects(counts, stress_metrics),
                    'hardware_utilization': self.calculate_hardware_utilization(transpiled_qc),
                    'error_mitigation_effectiveness': self.assess_error_mitigation(counts)
                })
                
                print(f"   ✅ Stress test completed")
                print(f"   📊 Hardware utilization: {result['hardware_utilization']['qubit_utilization']:.1%}")
                
            else:
                print(f"   ❌ Stress test failed: {job.status()}")
            
            return result
            
        except Exception as e:
            print(f"   ❌ Stress test error: {e}")
            return {
                'test_name': test_name,
                'error': str(e),
                'success': False,
                'timestamp': datetime.now().isoformat()
            }
    
    def calculate_stress_metrics(self, original: QuantumCircuit, transpiled: QuantumCircuit) -> Dict[str, Any]:
        """Calculate stress level metrics"""
        orig_gates = sum(original.count_ops().values())
        trans_gates = sum(transpiled.count_ops().values())
        
        # Stress factors
        depth_stress = transpiled.depth() / 100.0  # Normalize to 100 depth
        width_stress = transpiled.num_qubits / self.max_qubits
        gate_stress = trans_gates / 1000.0  # Normalize to 1000 gates
        
        # Overall stress level
        stress_level = (depth_stress + width_stress + gate_stress) / 3.0
        
        return {
            'depth_stress': min(1.0, depth_stress),
            'width_stress': width_stress,
            'gate_stress': min(1.0, gate_stress),
            'stress_level': min(1.0, stress_level),
            'gate_overhead': trans_gates / orig_gates if orig_gates > 0 else 1.0
        }
    
    def analyze_noise_effects(self, counts: Dict[str, int], stress_metrics: Dict[str, Any]) -> Dict[str, float]:
        """Analyze noise effects from measurement results"""
        if not counts:
            return {'noise_level': 1.0, 'signal_quality': 0.0}
        
        total = sum(counts.values())
        
        # Estimate noise from distribution uniformity
        n_outcomes = len(counts)
        expected_uniform = total / n_outcomes
        
        # Calculate deviation from uniform distribution
        deviations = [abs(count - expected_uniform) for count in counts.values()]
        avg_deviation = sum(deviations) / len(deviations)
        
        # Noise level (higher = more noise)
        noise_level = avg_deviation / expected_uniform if expected_uniform > 0 else 1.0
        
        # Signal quality (inverse of noise)
        signal_quality = max(0.0, 1.0 - noise_level)
        
        return {
            'noise_level': min(1.0, noise_level),
            'signal_quality': signal_quality,
            'distribution_uniformity': 1.0 / n_outcomes if n_outcomes > 0 else 0.0
        }
    
    def calculate_hardware_utilization(self, circuit: QuantumCircuit) -> Dict[str, float]:
        """Calculate hardware resource utilization"""
        qubit_utilization = circuit.num_qubits / self.max_qubits
        
        # Estimate gate utilization based on backend capabilities
        gate_counts = circuit.count_ops()
        total_gates = sum(gate_counts.values())
        
        # Rough estimate of gate capacity (backend dependent)
        estimated_gate_capacity = self.max_qubits * 100  # Rough estimate
        gate_utilization = total_gates / estimated_gate_capacity
        
        return {
            'qubit_utilization': qubit_utilization,
            'gate_utilization': min(1.0, gate_utilization),
            'depth_efficiency': circuit.depth() / total_gates if total_gates > 0 else 0.0
        }
    
    def assess_error_mitigation_effectiveness(self, counts: Dict[str, int]) -> Dict[str, float]:
        """Assess effectiveness of error mitigation"""
        if not counts:
            return {'mitigation_score': 0.0}
        
        # Simple assessment based on result quality
        total = sum(counts.values())
        max_count = max(counts.values())
        
        # Higher concentration suggests better error mitigation
        concentration = max_count / total if total > 0 else 0.0
        
        return {
            'mitigation_score': concentration,
            'result_concentration': concentration,
            'outcome_diversity': len(counts)
        }

def main():
    """Main execution for quantum hardware stress tests"""
    print("💪 Quantum Hardware Stress Test Suite")
    print("=" * 50)
    
    stress_tester = QuantumHardwareStressTest()
    
    if not stress_tester.connect_to_ibm():
        return 1
    
    # Stress test data
    secret_data = b"Quantum Hardware Stress Test 2025"
    
    # Stress test suite
    stress_tests = [
        ("Maximum_Depth_Circuit", stress_tester.create_maximum_depth_circuit(secret_data, 80)),
        ("Maximum_Width_Circuit", stress_tester.create_maximum_width_circuit(secret_data)),
        ("High_Gate_Count_Circuit", stress_tester.create_high_gate_count_circuit(secret_data, 800)),
        ("Noise_Resilient_Circuit", stress_tester.create_noise_resilient_circuit(secret_data))
    ]
    
    results = []
    
    for i, (name, circuit) in enumerate(stress_tests, 1):
        print(f"\n💪 Stress Test {i}/{len(stress_tests)}: {name}")
        print("-" * 60)
        
        result = stress_tester.execute_stress_test(name, circuit)
        results.append(result)
        
        # Extended pause for stress tests
        if i < len(stress_tests):
            print("⏳ Waiting 90s before next stress test...")
            time.sleep(90)
    
    # Parallel execution stress test
    print(f"\n💪 Parallel Execution Stress Test")
    print("-" * 60)
    
    parallel_circuits = stress_tester.create_parallel_execution_circuits(secret_data, 3)
    
    # Execute circuits in sequence (simulating parallel load)
    for i, circuit in enumerate(parallel_circuits):
        result = stress_tester.execute_stress_test(f"Parallel_Circuit_{i+1}", circuit, 500)
        results.append(result)
        time.sleep(30)  # Shorter pause for parallel tests
    
    # Generate stress test report
    successful = sum(1 for r in results if r.get('success', False))
    total = len(results)
    
    print(f"\n🎉 Quantum Hardware Stress Test Complete!")
    print("=" * 60)
    print(f"✅ Successful: {successful}/{total}")
    print(f"📊 Success Rate: {successful/total*100:.1f}%")
    print(f"💪 Hardware pushed to limits!")
    
    # Save stress test results
    report_data = {
        'stress_test_summary': {
            'total_tests': total,
            'successful_tests': successful,
            'backend_used': stress_tester.backend.name(),
            'max_qubits_available': stress_tester.max_qubits,
            'backend_properties': stress_tester.backend_properties,
            'timestamp': datetime.now().isoformat()
        },
        'stress_results': results
    }
    
    filename = f"quantum_hardware_stress_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(report_data, f, indent=2)
    
    print(f"📄 Stress test report saved: {filename}")
    
    return 0 if successful >= total * 0.8 else 1  # 80% success rate acceptable for stress tests

if __name__ == "__main__":
    exit(main())
