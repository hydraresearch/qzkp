#!/usr/bin/env python3
"""
Ultra-Fast Quantum Circuit Validation
Lightning-fast tests with 30s timeout for rapid validation
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
    from qiskit import QuantumCircuit, transpile, execute
    from qiskit.providers.ibmq import IBMQ
    from qiskit.providers import JobStatus
    from dotenv import load_dotenv
    print("✅ Ultra-fast packages loaded")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

class UltraFastValidator:
    """Ultra-fast quantum validation with 30s timeout"""
    
    def __init__(self):
        self.load_credentials()
        self.provider = None
        self.backend = None
        self.timeout = 30  # 30 second timeout
        self.results = []
        
    def load_credentials(self):
        """Load credentials"""
        env_path = os.path.join(os.path.dirname(__file__), '../../.env')
        load_dotenv(env_path)
        self.token = os.getenv('IBM_QUANTUM_TOKEN')
    
    def quick_connect(self):
        """Lightning-fast connection"""
        try:
            IBMQ.save_account(self.token, overwrite=True)
            IBMQ.load_account()
            self.provider = IBMQ.get_provider(hub='ibm-q')
            
            # Get any operational backend quickly
            backends = self.provider.backends(simulator=False, operational=True)
            self.backend = backends[0] if backends else None
            
            if self.backend:
                print(f"⚡ Connected to {self.backend.name()}")
                return True
            return False
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def create_minimal_zkp(self, data: bytes) -> QuantumCircuit:
        """Minimal ZKP circuit for ultra-fast execution"""
        qc = QuantumCircuit(2, 2)
        
        # Minimal encoding
        if hashlib.sha256(data).digest()[0] > 128:
            qc.x(0)
        
        # Minimal entanglement
        qc.h(0)
        qc.cx(0, 1)
        
        qc.measure_all()
        return qc
    
    def create_bell_test(self, data: bytes) -> QuantumCircuit:
        """Bell state test"""
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        
        # Data-dependent phase
        if hashlib.sha256(data).digest()[0] > 128:
            qc.z(0)
        
        qc.measure_all()
        return qc
    
    def create_single_qubit_test(self, data: bytes) -> QuantumCircuit:
        """Single qubit test"""
        qc = QuantumCircuit(1, 1)
        
        # Data-dependent rotation
        angle = (hashlib.sha256(data).digest()[0] / 255.0) * 2 * np.pi
        qc.ry(angle, 0)
        
        qc.measure_all()
        return qc
    
    def ultra_fast_execute(self, name: str, circuit: QuantumCircuit):
        """Ultra-fast execution with 30s timeout"""
        print(f"⚡ Ultra-fast: {name}")
        
        start_time = time.time()
        
        try:
            # Minimal transpile
            transpiled = transpile(circuit, self.backend, optimization_level=0)
            
            # Minimal shots for speed
            shots = 50
            
            job = execute(transpiled, self.backend, shots=shots)
            job_id = job.job_id()
            print(f"   Job: {job_id}")
            
            # Ultra-fast monitoring
            while job.status() not in [JobStatus.DONE, JobStatus.ERROR, JobStatus.CANCELLED]:
                elapsed = time.time() - start_time
                
                if elapsed > self.timeout:
                    print(f"   ⚡ TIMEOUT {elapsed:.1f}s")
                    try:
                        job.cancel()
                    except:
                        pass
                    
                    return {
                        'name': name,
                        'job_id': job_id,
                        'status': 'TIMEOUT',
                        'time': elapsed,
                        'success': False
                    }
                
                print(f"   {job.status()} ({elapsed:.1f}s)")
                time.sleep(3)  # Ultra-fast polling
            
            total_time = time.time() - start_time
            
            result = {
                'name': name,
                'job_id': job_id,
                'status': str(job.status()),
                'time': total_time,
                'success': job.status() == JobStatus.DONE
            }
            
            if job.status() == JobStatus.DONE:
                counts = job.result().get_counts()
                result['counts'] = counts
                result['outcomes'] = len(counts)
                print(f"   ✅ {total_time:.1f}s - {len(counts)} outcomes")
            else:
                print(f"   ❌ {job.status()}")
            
            return result
            
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"   ❌ ERROR {elapsed:.1f}s: {e}")
            
            return {
                'name': name,
                'error': str(e),
                'time': elapsed,
                'success': False
            }
    
    def run_ultra_fast_suite(self):
        """Run ultra-fast test suite"""
        print("⚡ Ultra-Fast Validation Suite (30s timeout)")
        print("=" * 50)
        
        if not self.quick_connect():
            return []
        
        # Ultra-fast test data
        data = b"Ultra Fast Test"
        
        # Minimal test cases
        tests = [
            ("Minimal_ZKP", self.create_minimal_zkp(data)),
            ("Bell_Test", self.create_bell_test(data)),
            ("Single_Qubit", self.create_single_qubit_test(data)),
            ("Minimal_ZKP_2", self.create_minimal_zkp(data + b"_2")),
        ]
        
        for i, (name, circuit) in enumerate(tests, 1):
            print(f"\n⚡ Test {i}/{len(tests)}: {name}")
            print("-" * 30)
            
            result = self.ultra_fast_execute(name, circuit)
            self.results.append(result)
            
            # Minimal pause
            if i < len(tests):
                print("⏳ 5s...")
                time.sleep(5)
        
        return self.results
    
    def generate_ultra_fast_report(self):
        """Generate ultra-fast report"""
        successful = sum(1 for r in self.results if r.get('success', False))
        total = len(self.results)
        
        times = [r.get('time', 0) for r in self.results]
        avg_time = np.mean(times) if times else 0
        
        summary = {
            'total': total,
            'successful': successful,
            'success_rate': (successful / total * 100) if total > 0 else 0,
            'avg_time': avg_time,
            'max_time': max(times) if times else 0,
            'job_ids': [r.get('job_id', 'N/A') for r in self.results if 'job_id' in r]
        }
        
        print(f"\n⚡ Ultra-Fast Suite Complete!")
        print("=" * 40)
        print(f"✅ Success: {successful}/{total} ({successful/total*100:.1f}%)")
        print(f"⚡ Avg Time: {avg_time:.1f}s")
        print(f"🏃 Max Time: {max(times) if times else 0:.1f}s")
        
        # Save minimal report
        filename = f"ultra_fast_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump({
                'summary': summary,
                'results': self.results,
                'timestamp': datetime.now().isoformat()
            }, f, indent=2)
        
        print(f"📄 Report: {filename}")
        
        return successful == total

def main():
    """Ultra-fast main execution"""
    print("⚡ Ultra-Fast Quantum Validation")
    print("=" * 35)
    
    validator = UltraFastValidator()
    
    try:
        results = validator.run_ultra_fast_suite()
        success = validator.generate_ultra_fast_report()
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted")
        return 1
    except Exception as e:
        print(f"\n❌ Failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
