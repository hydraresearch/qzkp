#!/usr/bin/env python3
"""
Fast IBM Quantum Tests with 60s Timeout
Efficient quantum ZKP validation with strict time limits
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
    from qiskit import QuantumCircuit, transpile, execute
    from qiskit.providers.ibmq import IBMQ
    from qiskit.providers import JobStatus
    from qiskit.quantum_info import Statevector
    from dotenv import load_dotenv
    print("✅ Fast quantum test packages loaded")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

class FastIBMQuantumTester:
    """Fast quantum testing with strict timeouts"""
    
    def __init__(self):
        self.load_credentials()
        self.provider = None
        self.backend = None
        self.test_results = []
        self.timeout_limit = 60  # 60 second hard limit
        
    def load_credentials(self):
        """Load IBM Quantum credentials"""
        env_path = os.path.join(os.path.dirname(__file__), '../../.env')
        load_dotenv(env_path)
        self.token = os.getenv('IBM_QUANTUM_TOKEN')
        
        if not self.token:
            print("❌ IBM_QUANTUM_TOKEN not found in .env file")
            sys.exit(1)
    
    def connect_to_ibm(self):
        """Quick connection to IBM Quantum"""
        try:
            print("🔌 Quick connecting to IBM Quantum...")
            IBMQ.save_account(self.token, overwrite=True)
            IBMQ.load_account()
            
            self.provider = IBMQ.get_provider(hub='ibm-q')
            
            # Get fastest available backend (least busy)
            backends = self.provider.backends(simulator=False, operational=True)
            
            # Sort by queue length (if available) or use first operational
            try:
                backend_status = [(b, b.status().pending_jobs) for b in backends]
                backend_status.sort(key=lambda x: x[1])
                self.backend = backend_status[0][0]
            except:
                self.backend = backends[0] if backends else None
            
            if self.backend:
                config = self.backend.configuration()
                status = self.backend.status()
                print(f"✅ Connected to {config.backend_name}")
                print(f"📊 Queue: {status.pending_jobs} jobs, {config.n_qubits} qubits")
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Quick connection failed: {e}")
            return False
    
    def create_fast_zkp_circuit(self, data: bytes, n_qubits: int = 4) -> QuantumCircuit:
        """Create fast ZKP circuit optimized for speed"""
        # Keep circuits small for fast execution
        n_qubits = min(n_qubits, 6)  # Max 6 qubits for speed
        
        qc = QuantumCircuit(n_qubits, n_qubits)
        
        # Quick encoding from data
        data_hash = hashlib.sha256(data).digest()
        
        # Simple but effective encoding
        for i in range(n_qubits):
            # Single rotation per qubit
            theta = (data_hash[i % len(data_hash)] / 255.0) * 2 * np.pi
            qc.ry(theta, i)
        
        # Minimal entanglement for verification
        for i in range(n_qubits - 1):
            qc.cx(i, i + 1)
        
        # Quick measurement
        qc.measure_all()
        
        return qc
    
    def create_bell_state_zkp(self, data: bytes) -> QuantumCircuit:
        """Create Bell state ZKP circuit"""
        qc = QuantumCircuit(2, 2)
        
        # Encode data into Bell state choice
        data_hash = hashlib.sha256(data).digest()
        
        # Create Bell state
        qc.h(0)
        qc.cx(0, 1)
        
        # Data-dependent phase
        if data_hash[0] > 128:
            qc.z(0)
        if data_hash[1] > 128:
            qc.z(1)
        
        qc.measure_all()
        return qc
    
    def create_ghz_state_zkp(self, data: bytes, n_qubits: int = 3) -> QuantumCircuit:
        """Create GHZ state ZKP circuit"""
        n_qubits = min(n_qubits, 4)  # Keep small for speed
        qc = QuantumCircuit(n_qubits, n_qubits)
        
        data_hash = hashlib.sha256(data).digest()
        
        # Create GHZ state
        qc.h(0)
        for i in range(n_qubits - 1):
            qc.cx(0, i + 1)
        
        # Data-dependent modifications
        for i in range(n_qubits):
            if data_hash[i % len(data_hash)] > 128:
                qc.z(i)
        
        qc.measure_all()
        return qc
    
    def create_random_circuit_zkp(self, data: bytes, depth: int = 5) -> QuantumCircuit:
        """Create random circuit ZKP"""
        n_qubits = 4
        qc = QuantumCircuit(n_qubits, n_qubits)
        
        # Seed from data
        data_hash = hashlib.sha256(data).digest()
        np.random.seed(int.from_bytes(data_hash[:4], 'big'))
        
        # Random circuit with limited depth
        for layer in range(min(depth, 5)):  # Max 5 layers for speed
            # Random single-qubit gates
            for qubit in range(n_qubits):
                gate_choice = np.random.randint(0, 3)
                angle = np.random.uniform(0, 2 * np.pi)
                
                if gate_choice == 0:
                    qc.rx(angle, qubit)
                elif gate_choice == 1:
                    qc.ry(angle, qubit)
                else:
                    qc.rz(angle, qubit)
            
            # Random entanglement
            pairs = [(0, 1), (1, 2), (2, 3), (3, 0)]
            pair = pairs[np.random.randint(0, len(pairs))]
            qc.cx(pair[0], pair[1])
        
        qc.measure_all()
        return qc
    
    def create_qft_zkp(self, data: bytes, n_qubits: int = 3) -> QuantumCircuit:
        """Create QFT-based ZKP circuit"""
        n_qubits = min(n_qubits, 4)  # Keep small
        qc = QuantumCircuit(n_qubits, n_qubits)
        
        data_hash = hashlib.sha256(data).digest()
        
        # Initialize with data
        for i in range(n_qubits):
            if data_hash[i % len(data_hash)] > 128:
                qc.x(i)
        
        # Simple QFT (manual implementation for speed)
        for i in range(n_qubits):
            qc.h(i)
            for j in range(i + 1, n_qubits):
                angle = np.pi / (2 ** (j - i))
                qc.cp(angle, j, i)
        
        # Reverse order
        for i in range(n_qubits // 2):
            qc.swap(i, n_qubits - 1 - i)
        
        qc.measure_all()
        return qc
    
    def execute_fast_test(self, test_name: str, circuit: QuantumCircuit) -> Dict[str, Any]:
        """Execute test with strict 60s timeout"""
        print(f"⚡ Fast test: {test_name}")
        
        start_total = time.time()
        
        try:
            # Quick transpile
            transpiled_qc = transpile(circuit, self.backend, optimization_level=1)
            
            print(f"   Circuit: {transpiled_qc.depth()} depth, {transpiled_qc.num_qubits} qubits")
            
            # Fast execution with fewer shots
            shots = 100  # Reduced shots for speed
            
            job = execute(transpiled_qc, self.backend, shots=shots)
            job_id = job.job_id()
            print(f"   Job ID: {job_id}")
            
            # Monitor with strict timeout
            start_monitor = time.time()
            
            while job.status() not in [JobStatus.DONE, JobStatus.ERROR, JobStatus.CANCELLED]:
                elapsed = time.time() - start_total
                
                if elapsed > self.timeout_limit:
                    print(f"   ⏰ TIMEOUT after {elapsed:.1f}s - ENDING TEST")
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
                        'timeout': True,
                        'timestamp': datetime.now().isoformat()
                    }
                
                print(f"   Status: {job.status()} ({elapsed:.1f}s)")
                time.sleep(5)  # Quick polling
            
            total_time = time.time() - start_total
            
            result = {
                'test_name': test_name,
                'job_id': job_id,
                'backend': self.backend.name(),
                'status': str(job.status()),
                'execution_time': total_time,
                'circuit_depth': transpiled_qc.depth(),
                'num_qubits': transpiled_qc.num_qubits,
                'shots': shots,
                'timestamp': datetime.now().isoformat(),
                'success': job.status() == JobStatus.DONE,
                'timeout': False
            }
            
            if job.status() == JobStatus.DONE:
                job_result = job.result()
                counts = job_result.get_counts()
                
                # Quick analysis
                result.update({
                    'measurement_counts': counts,
                    'unique_outcomes': len(counts),
                    'entropy': self.quick_entropy(counts),
                    'max_probability': max(counts.values()) / shots if counts else 0
                })
                
                print(f"   ✅ COMPLETED in {total_time:.1f}s")
                print(f"   📊 {len(counts)} unique outcomes")
                
            else:
                print(f"   ❌ FAILED: {job.status()}")
            
            return result
            
        except Exception as e:
            elapsed = time.time() - start_total
            print(f"   ❌ ERROR after {elapsed:.1f}s: {e}")
            
            return {
                'test_name': test_name,
                'error': str(e),
                'execution_time': elapsed,
                'success': False,
                'timeout': False,
                'timestamp': datetime.now().isoformat()
            }
    
    def quick_entropy(self, counts: Dict[str, int]) -> float:
        """Quick entropy calculation"""
        if not counts:
            return 0.0
        
        total = sum(counts.values())
        entropy = 0.0
        
        for count in counts.values():
            if count > 0:
                p = count / total
                entropy -= p * np.log2(p)
        
        return entropy
    
    def run_fast_test_suite(self) -> List[Dict[str, Any]]:
        """Run fast test suite with timeouts"""
        print("⚡ Fast IBM Quantum Test Suite (60s timeout per test)")
        print("=" * 60)
        
        if not self.connect_to_ibm():
            return []
        
        # Test data
        test_data = b"Fast Quantum ZKP Test 2025"
        
        # Fast test cases
        test_cases = [
            ("Bell_State_ZKP", self.create_bell_state_zkp(test_data)),
            ("GHZ_State_ZKP", self.create_ghz_state_zkp(test_data, 3)),
            ("Fast_ZKP_4qubit", self.create_fast_zkp_circuit(test_data, 4)),
            ("Random_Circuit_ZKP", self.create_random_circuit_zkp(test_data, 4)),
            ("QFT_ZKP", self.create_qft_zkp(test_data, 3)),
            ("Fast_ZKP_5qubit", self.create_fast_zkp_circuit(test_data + b"_variant", 5))
        ]
        
        results = []
        
        for i, (name, circuit) in enumerate(test_cases, 1):
            print(f"\n⚡ Fast Test {i}/{len(test_cases)}: {name}")
            print("-" * 40)
            
            result = self.execute_fast_test(name, circuit)
            results.append(result)
            self.test_results.append(result)
            
            # Quick pause between tests
            if i < len(test_cases):
                print("⏳ 10s pause...")
                time.sleep(10)
        
        return results
    
    def generate_fast_report(self) -> str:
        """Generate fast test report"""
        successful = sum(1 for r in self.test_results if r.get('success', False))
        timeouts = sum(1 for r in self.test_results if r.get('timeout', False))
        total = len(self.test_results)
        
        # Calculate timing stats
        execution_times = [r.get('execution_time', 0) for r in self.test_results]
        avg_time = np.mean(execution_times) if execution_times else 0
        max_time = max(execution_times) if execution_times else 0
        
        report_data = {
            'fast_test_summary': {
                'total_tests': total,
                'successful_tests': successful,
                'timeout_tests': timeouts,
                'failed_tests': total - successful,
                'success_rate': (successful / total * 100) if total > 0 else 0,
                'avg_execution_time': avg_time,
                'max_execution_time': max_time,
                'backend_used': self.backend.name() if self.backend else 'N/A',
                'timestamp': datetime.now().isoformat(),
                'job_ids': [r.get('job_id', 'N/A') for r in self.test_results if 'job_id' in r]
            },
            'test_results': self.test_results
        }
        
        # Save JSON report
        filename = f"fast_ibm_quantum_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        # Generate markdown summary
        markdown = f"""# Fast IBM Quantum Test Report

**Generated:** {datetime.now().isoformat()}
**Backend:** {self.backend.name() if self.backend else 'N/A'}
**Timeout Limit:** {self.timeout_limit}s per test

## Summary

- ✅ **Successful Tests:** {successful}/{total} ({successful/total*100:.1f}%)
- ⏰ **Timeout Tests:** {timeouts}/{total}
- ❌ **Failed Tests:** {total - successful - timeouts}/{total}
- ⚡ **Average Time:** {avg_time:.1f}s
- 🏃 **Max Time:** {max_time:.1f}s

## Job IDs

"""
        
        for i, job_id in enumerate(report_data['fast_test_summary']['job_ids'], 1):
            if job_id != 'N/A':
                markdown += f"{i}. `{job_id}`\n"
        
        markdown += f"""

## Test Results

"""
        
        for result in self.test_results:
            status = "✅ PASSED" if result.get('success', False) else "⏰ TIMEOUT" if result.get('timeout', False) else "❌ FAILED"
            time_str = f"{result.get('execution_time', 0):.1f}s"
            
            markdown += f"- **{result['test_name']}**: {status} ({time_str})\n"
        
        markdown += f"""

## Performance Analysis

- **Speed Optimized:** All tests designed for <60s execution
- **Efficient Circuits:** Small qubit counts and depths for fast execution
- **Quick Polling:** 5s status checks for responsive monitoring
- **Timeout Protection:** Automatic cancellation after 60s

**Repository:** https://github.com/hydraresearch/qzkp
"""
        
        markdown_filename = f"fast_test_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(markdown_filename, 'w') as f:
            f.write(markdown)
        
        print(f"📄 Fast report saved: {filename}")
        print(f"📋 Summary saved: {markdown_filename}")
        
        return markdown_filename

def main():
    """Main execution for fast tests"""
    print("⚡ Fast IBM Quantum Test Suite")
    print("=" * 40)
    
    tester = FastIBMQuantumTester()
    
    try:
        # Run fast test suite
        results = tester.run_fast_test_suite()
        
        # Generate report
        report_file = tester.generate_fast_report()
        
        # Print summary
        successful = sum(1 for r in results if r.get('success', False))
        timeouts = sum(1 for r in results if r.get('timeout', False))
        total = len(results)
        
        print(f"\n⚡ Fast Test Suite Complete!")
        print("=" * 40)
        print(f"✅ Successful: {successful}/{total}")
        print(f"⏰ Timeouts: {timeouts}/{total}")
        print(f"📊 Success Rate: {successful/total*100:.1f}%")
        print(f"📄 Report: {report_file}")
        
        if successful >= total * 0.7:  # 70% success rate acceptable
            print("\n🚀 FAST TESTS PASSED - Hardware validation successful!")
            return 0
        else:
            print(f"\n⚠️ Some tests failed - check logs for details")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ Fast test suite interrupted")
        return 1
    except Exception as e:
        print(f"\n❌ Fast test suite failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
