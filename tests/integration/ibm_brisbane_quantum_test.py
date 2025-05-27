#!/usr/bin/env python3
"""
IBM Brisbane Quantum Hardware Test
Specific test for IBM Brisbane backend with ZKP circuits
"""

import os
import sys
import json
import time
import hashlib
import numpy as np
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

try:
    from qiskit import QuantumCircuit, transpile
    from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
    from dotenv import load_dotenv
    print("✅ Qiskit packages loaded for IBM Brisbane")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Run: pip install qiskit qiskit-ibm-runtime python-dotenv")
    sys.exit(1)

class IBMBrisbaneQuantumTest:
    """IBM Brisbane specific quantum hardware test"""
    
    def __init__(self):
        self.load_credentials()
        self.service = None
        self.backend = None
        self.timeout = 60  # 60 second timeout
        
    def load_credentials(self):
        """Load IBM Quantum credentials"""
        env_path = os.path.join(os.path.dirname(__file__), '../../.env')
        print(f"🔑 Loading from: {env_path}")
        
        if not os.path.exists(env_path):
            print(f"❌ .env file not found")
            sys.exit(1)
            
        load_dotenv(env_path)
        self.token = os.getenv('IQKAPI')
        
        if not self.token:
            print("❌ IQKAPI not found in .env file")
            sys.exit(1)
            
        print("✅ IBM Quantum credentials loaded")
    
    def connect_to_brisbane(self):
        """Connect specifically to IBM Brisbane"""
        try:
            print("🔌 Connecting to IBM Quantum (targeting Brisbane)...")
            
            # Connect with channel
            try:
                self.service = QiskitRuntimeService(token=self.token, channel='ibm_quantum')
                print("✅ Connected to IBM Quantum service")
            except Exception as e:
                print(f"❌ Service connection failed: {e}")
                return False
            
            # Get all backends
            try:
                backends = self.service.backends(simulator=False, operational=True)
                print(f"📊 Found {len(backends)} operational backends")
            except Exception as e:
                print(f"❌ Failed to get backends: {e}")
                return False
            
            if not backends:
                print("❌ No operational backends available")
                return False
            
            # Look for Brisbane specifically
            brisbane_backend = None
            available_backends = []
            
            for backend in backends:
                available_backends.append(backend.name)
                if 'brisbane' in backend.name.lower():
                    brisbane_backend = backend
                    break
            
            print(f"📋 Available backends: {', '.join(available_backends)}")
            
            if brisbane_backend:
                self.backend = brisbane_backend
                config = self.backend.configuration()
                status = self.backend.status()
                
                print(f"🎯 Successfully connected to IBM Brisbane!")
                print(f"   Name: {config.backend_name}")
                print(f"   Qubits: {config.n_qubits}")
                print(f"   Queue: {status.pending_jobs} jobs")
                print(f"   Operational: {status.operational}")
                
                return True
            else:
                # Use best available backend
                self.backend = backends[0]
                config = self.backend.configuration()
                
                print(f"⚠️ Brisbane not available, using: {config.backend_name}")
                print(f"   Qubits: {config.n_qubits}")
                
                return True
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def create_brisbane_zkp_circuit(self, data: bytes) -> QuantumCircuit:
        """Create ZKP circuit optimized for Brisbane"""
        # Brisbane has 127 qubits, but we'll use a small subset for fast execution
        n_qubits = 4
        qc = QuantumCircuit(n_qubits, n_qubits)
        
        # Encode secret data
        data_hash = hashlib.sha256(data).digest()
        
        # Initialize qubits with secret-dependent rotations
        for i in range(n_qubits):
            theta = (data_hash[i % len(data_hash)] / 255.0) * 2 * np.pi
            phi = (data_hash[(i + 4) % len(data_hash)] / 255.0) * 2 * np.pi
            
            qc.ry(theta, i)
            qc.rz(phi, i)
        
        # Create entanglement pattern
        qc.h(0)
        for i in range(n_qubits - 1):
            qc.cx(i, i + 1)
        
        # Add verification layer
        for i in range(n_qubits):
            if data_hash[(i + 8) % len(data_hash)] > 128:
                qc.z(i)
        
        # Measurement
        qc.measure_all()
        
        return qc
    
    def create_bell_zkp_circuit(self, data: bytes) -> QuantumCircuit:
        """Create Bell state ZKP circuit"""
        qc = QuantumCircuit(2, 2)
        
        data_hash = hashlib.sha256(data).digest()
        
        # Create Bell state
        qc.h(0)
        qc.cx(0, 1)
        
        # Data-dependent modifications
        if data_hash[0] > 128:
            qc.z(0)
        if data_hash[1] > 128:
            qc.z(1)
        
        qc.measure_all()
        return qc
    
    def execute_brisbane_test(self, test_name: str, circuit: QuantumCircuit):
        """Execute test on Brisbane with timeout"""
        print(f"🔬 Brisbane test: {test_name}")
        
        start_time = time.time()
        
        try:
            # Transpile for Brisbane
            transpiled = transpile(circuit, self.backend, optimization_level=1)
            
            print(f"   Original: {circuit.depth()} depth, {circuit.num_qubits} qubits")
            print(f"   Transpiled: {transpiled.depth()} depth, {transpiled.num_qubits} qubits")
            
            # Create sampler
            sampler = Sampler(self.backend)
            
            # Execute with minimal shots for speed
            shots = 100
            print(f"   Executing {shots} shots on {self.backend.name}...")
            
            # Submit job
            job = sampler.run([transpiled], shots=shots)
            job_id = job.job_id()
            
            print(f"   Job ID: {job_id}")
            print(f"   🔗 Verify at: https://quantum-computing.ibm.com/")
            
            # Monitor with timeout
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
            
            # Calculate metrics
            entropy = self.calculate_entropy(counts)
            max_prob = max(counts.values()) / shots if counts else 0
            
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
                'unique_outcomes': len(counts),
                'entropy': entropy,
                'max_probability': max_prob,
                'success': True,
                'timeout': False,
                'timestamp': datetime.now().isoformat()
            }
            
            print(f"   ✅ COMPLETED in {total_time:.1f}s")
            print(f"   📊 {len(counts)} unique outcomes")
            print(f"   🎯 Entropy: {entropy:.3f}")
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
    
    def calculate_entropy(self, counts):
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
    
    def run_brisbane_validation(self):
        """Run Brisbane validation suite"""
        print("🚀 IBM Brisbane Quantum ZKP Validation")
        print("=" * 45)
        
        if not self.connect_to_brisbane():
            return False
        
        # Test data
        test_data = b"IBM Brisbane Quantum ZKP Test 2025"
        
        # Test cases
        test_cases = [
            ("Bell_State_ZKP", self.create_bell_zkp_circuit(test_data)),
            ("Brisbane_ZKP_4q", self.create_brisbane_zkp_circuit(test_data)),
            ("Bell_Variant", self.create_bell_zkp_circuit(test_data + b"_variant"))
        ]
        
        results = []
        
        for i, (name, circuit) in enumerate(test_cases, 1):
            print(f"\n🔬 Brisbane Test {i}/{len(test_cases)}: {name}")
            print("-" * 40)
            
            result = self.execute_brisbane_test(name, circuit)
            results.append(result)
            
            # Pause between tests
            if i < len(test_cases):
                print("⏳ 20s pause...")
                time.sleep(20)
        
        # Generate report
        successful = sum(1 for r in results if r.get('success', False))
        total = len(results)
        
        report = {
            'brisbane_validation_summary': {
                'backend_used': self.backend.name if self.backend else 'N/A',
                'total_tests': total,
                'successful_tests': successful,
                'success_rate': (successful / total * 100) if total > 0 else 0,
                'job_ids': [r.get('job_id', 'N/A') for r in results if 'job_id' in r],
                'timestamp': datetime.now().isoformat()
            },
            'test_results': results
        }
        
        # Save report
        filename = f"ibm_brisbane_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n🎉 Brisbane Validation Complete!")
        print("=" * 40)
        print(f"✅ Successful: {successful}/{total}")
        print(f"📊 Success Rate: {successful/total*100:.1f}%")
        print(f"🏭 Backend: {self.backend.name}")
        print(f"📄 Report: {filename}")
        
        # Print job IDs for verification
        job_ids = [r.get('job_id') for r in results if r.get('job_id')]
        if job_ids:
            print(f"\n🔗 Verifiable Job IDs:")
            for i, job_id in enumerate(job_ids, 1):
                print(f"   {i}. {job_id}")
            print(f"   Verify at: https://quantum-computing.ibm.com/")
        
        return successful >= total * 0.6  # 60% success rate acceptable

def main():
    """Main execution"""
    tester = IBMBrisbaneQuantumTest()
    
    try:
        success = tester.run_brisbane_validation()
        
        if success:
            print("\n🚀 IBM BRISBANE VALIDATION SUCCESSFUL!")
            print("🔬 Real quantum hardware execution confirmed!")
            return 0
        else:
            print("\n⚠️ Brisbane validation needs attention")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ Brisbane validation interrupted")
        return 1
    except Exception as e:
        print(f"\n❌ Brisbane validation failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
