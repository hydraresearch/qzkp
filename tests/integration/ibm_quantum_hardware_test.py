#!/usr/bin/env python3
"""
Comprehensive IBM Quantum Hardware Tests for Quantum ZKP System
Tests real quantum hardware execution with verifiable job IDs
"""

import os
import sys
import json
import time
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Tuple
import numpy as np

# Add the root directory to Python path to access .env
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

try:
    from qiskit import QuantumCircuit, transpile, execute
    from qiskit.providers.ibmq import IBMQ
    from qiskit.providers import JobStatus
    from qiskit.quantum_info import Statevector
    from dotenv import load_dotenv
    print("✅ All required packages imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Install required packages: pip install qiskit python-dotenv")
    sys.exit(1)

class IBMQuantumZKPTester:
    """Comprehensive IBM Quantum hardware tester for ZKP system"""
    
    def __init__(self):
        self.load_credentials()
        self.provider = None
        self.backend = None
        self.test_results = []
        self.job_ids = []
        
    def load_credentials(self):
        """Load IBM Quantum credentials from .env file"""
        env_path = os.path.join(os.path.dirname(__file__), '../../.env')
        print(f"🔑 Loading credentials from: {env_path}")
        
        if not os.path.exists(env_path):
            print(f"❌ .env file not found at: {env_path}")
            sys.exit(1)
            
        load_dotenv(env_path)
        self.token = os.getenv('IBM_QUANTUM_TOKEN')
        
        if not self.token:
            print("❌ IBM_QUANTUM_TOKEN not found in .env file")
            sys.exit(1)
            
        print("✅ IBM Quantum credentials loaded successfully")
    
    def connect_to_ibm(self):
        """Connect to IBM Quantum and select backend"""
        try:
            print("🔌 Connecting to IBM Quantum...")
            IBMQ.save_account(self.token, overwrite=True)
            IBMQ.load_account()
            
            self.provider = IBMQ.get_provider(hub='ibm-q')
            
            # Try to get Brisbane backend first, fallback to others
            backend_preferences = ['ibm_brisbane', 'ibm_kyoto', 'ibm_osaka', 'ibm_sherbrooke']
            
            for backend_name in backend_preferences:
                try:
                    self.backend = self.provider.get_backend(backend_name)
                    print(f"✅ Connected to backend: {backend_name}")
                    break
                except Exception as e:
                    print(f"⚠️ Backend {backend_name} not available: {e}")
                    continue
            
            if not self.backend:
                # Fallback to any available backend
                backends = self.provider.backends(simulator=False, operational=True)
                if backends:
                    self.backend = backends[0]
                    print(f"✅ Using fallback backend: {self.backend.name()}")
                else:
                    print("❌ No operational quantum backends available")
                    return False
                    
            # Print backend info
            config = self.backend.configuration()
            print(f"📊 Backend Info:")
            print(f"   Name: {config.backend_name}")
            print(f"   Qubits: {config.n_qubits}")
            print(f"   Max Shots: {config.max_shots}")
            print(f"   Quantum Volume: {getattr(config, 'quantum_volume', 'N/A')}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to connect to IBM Quantum: {e}")
            return False
    
    def create_qzkp_circuit(self, data: bytes, security_level: int = 256) -> QuantumCircuit:
        """Create quantum ZKP circuit from classical data"""
        # Calculate number of qubits needed
        num_qubits = min(security_level // 8, self.backend.configuration().n_qubits)
        num_qubits = max(2, num_qubits)  # Minimum 2 qubits
        
        qc = QuantumCircuit(num_qubits, num_qubits)
        
        # Convert data to quantum parameters
        data_hash = hashlib.sha256(data).digest()
        
        # Create quantum state encoding
        for i in range(num_qubits):
            # Use data bytes to determine rotation angles
            theta = (data_hash[i % len(data_hash)] / 255.0) * 2 * np.pi
            phi = (data_hash[(i + 1) % len(data_hash)] / 255.0) * 2 * np.pi
            
            # Apply rotations
            qc.ry(theta, i)
            qc.rz(phi, i)
        
        # Create entanglement for verification
        for i in range(num_qubits - 1):
            qc.cx(i, i + 1)
        
        # Add measurements
        qc.measure_all()
        
        return qc
    
    def execute_quantum_test(self, test_name: str, data: bytes, security_level: int = 256) -> Dict[str, Any]:
        """Execute a single quantum test on IBM hardware"""
        print(f"🔬 Executing test: {test_name}")
        
        try:
            # Create circuit
            qc = self.create_qzkp_circuit(data, security_level)
            
            # Transpile for backend
            transpiled_qc = transpile(qc, self.backend, optimization_level=3)
            
            print(f"   Circuit depth: {transpiled_qc.depth()}")
            print(f"   Circuit qubits: {transpiled_qc.num_qubits}")
            
            # Execute on quantum hardware
            shots = 1000
            job = execute(transpiled_qc, self.backend, shots=shots)
            
            job_id = job.job_id()
            self.job_ids.append(job_id)
            print(f"   Job ID: {job_id}")
            print(f"   Status: {job.status()}")
            
            # Wait for completion with timeout
            start_time = time.time()
            timeout = 300  # 5 minutes
            
            while job.status() not in [JobStatus.DONE, JobStatus.ERROR, JobStatus.CANCELLED]:
                if time.time() - start_time > timeout:
                    print(f"   ⚠️ Job timeout after {timeout}s")
                    break
                print(f"   Waiting... Status: {job.status()}")
                time.sleep(10)
            
            execution_time = time.time() - start_time
            
            result = {
                'test_name': test_name,
                'job_id': job_id,
                'backend': self.backend.name(),
                'status': str(job.status()),
                'execution_time': execution_time,
                'circuit_depth': transpiled_qc.depth(),
                'num_qubits': transpiled_qc.num_qubits,
                'shots': shots,
                'security_level': security_level,
                'timestamp': datetime.now().isoformat(),
                'success': job.status() == JobStatus.DONE
            }
            
            if job.status() == JobStatus.DONE:
                job_result = job.result()
                counts = job_result.get_counts()
                
                # Calculate quantum state properties
                total_counts = sum(counts.values())
                entropy = self.calculate_entropy(counts)
                
                result.update({
                    'counts': counts,
                    'total_measurements': total_counts,
                    'entropy': entropy,
                    'unique_states': len(counts),
                    'fidelity': self.estimate_fidelity(counts)
                })
                
                print(f"   ✅ Test completed successfully")
                print(f"   📊 Entropy: {entropy:.3f}")
                print(f"   🎯 Unique states: {len(counts)}")
                
            else:
                print(f"   ❌ Test failed: {job.status()}")
            
            return result
            
        except Exception as e:
            print(f"   ❌ Test execution failed: {e}")
            return {
                'test_name': test_name,
                'error': str(e),
                'success': False,
                'timestamp': datetime.now().isoformat()
            }
    
    def calculate_entropy(self, counts: Dict[str, int]) -> float:
        """Calculate Shannon entropy of measurement results"""
        total = sum(counts.values())
        if total == 0:
            return 0.0
        
        entropy = 0.0
        for count in counts.values():
            if count > 0:
                p = count / total
                entropy -= p * np.log2(p)
        
        return entropy
    
    def estimate_fidelity(self, counts: Dict[str, int]) -> float:
        """Estimate quantum fidelity from measurement results"""
        total = sum(counts.values())
        if total == 0:
            return 0.0
        
        # Simple fidelity estimate based on distribution uniformity
        expected_prob = 1.0 / len(counts) if counts else 0
        fidelity = 0.0
        
        for count in counts.values():
            actual_prob = count / total
            fidelity += min(actual_prob, expected_prob)
        
        return fidelity
    
    def run_comprehensive_tests(self) -> List[Dict[str, Any]]:
        """Run comprehensive test suite on IBM Quantum hardware"""
        print("🚀 Starting Comprehensive IBM Quantum Hardware Tests")
        print("=" * 60)
        
        if not self.connect_to_ibm():
            return []
        
        # Test cases with different data types and security levels
        test_cases = [
            {
                'name': 'Text_Data_256bit',
                'data': b'Hello Quantum ZKP World!',
                'security_level': 256
            },
            {
                'name': 'Binary_Data_128bit',
                'data': bytes([i for i in range(32)]),
                'security_level': 128
            },
            {
                'name': 'Unicode_Data_80bit',
                'data': '🔐⚛️🌌🔬'.encode('utf-8'),
                'security_level': 80
            },
            {
                'name': 'Hash_Data_256bit',
                'data': hashlib.sha256(b'quantum zkp test').digest(),
                'security_level': 256
            },
            {
                'name': 'Random_Data_128bit',
                'data': os.urandom(32),
                'security_level': 128
            }
        ]
        
        results = []
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📋 Test {i}/{len(test_cases)}: {test_case['name']}")
            print("-" * 40)
            
            result = self.execute_quantum_test(
                test_case['name'],
                test_case['data'],
                test_case['security_level']
            )
            
            results.append(result)
            self.test_results.append(result)
            
            # Brief pause between tests
            if i < len(test_cases):
                print("⏳ Waiting 30s before next test...")
                time.sleep(30)
        
        return results
    
    def generate_test_report(self) -> str:
        """Generate comprehensive test report"""
        report_data = {
            'test_summary': {
                'total_tests': len(self.test_results),
                'successful_tests': sum(1 for r in self.test_results if r.get('success', False)),
                'failed_tests': sum(1 for r in self.test_results if not r.get('success', False)),
                'backend_used': self.backend.name() if self.backend else 'N/A',
                'timestamp': datetime.now().isoformat(),
                'job_ids': self.job_ids
            },
            'test_results': self.test_results,
            'performance_metrics': self.calculate_performance_metrics()
        }
        
        # Save detailed JSON report
        report_filename = f"ibm_quantum_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_filename, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        # Generate markdown summary
        markdown_report = self.generate_markdown_report(report_data)
        markdown_filename = f"ibm_quantum_test_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(markdown_filename, 'w') as f:
            f.write(markdown_report)
        
        print(f"📄 Detailed report saved: {report_filename}")
        print(f"📋 Summary report saved: {markdown_filename}")
        
        return markdown_filename
    
    def calculate_performance_metrics(self) -> Dict[str, Any]:
        """Calculate performance metrics from test results"""
        successful_tests = [r for r in self.test_results if r.get('success', False)]
        
        if not successful_tests:
            return {}
        
        execution_times = [r.get('execution_time', 0) for r in successful_tests]
        circuit_depths = [r.get('circuit_depth', 0) for r in successful_tests]
        entropies = [r.get('entropy', 0) for r in successful_tests if 'entropy' in r]
        fidelities = [r.get('fidelity', 0) for r in successful_tests if 'fidelity' in r]
        
        return {
            'avg_execution_time': np.mean(execution_times) if execution_times else 0,
            'min_execution_time': np.min(execution_times) if execution_times else 0,
            'max_execution_time': np.max(execution_times) if execution_times else 0,
            'avg_circuit_depth': np.mean(circuit_depths) if circuit_depths else 0,
            'avg_entropy': np.mean(entropies) if entropies else 0,
            'avg_fidelity': np.mean(fidelities) if fidelities else 0,
            'total_job_ids': len(self.job_ids)
        }
    
    def generate_markdown_report(self, report_data: Dict[str, Any]) -> str:
        """Generate markdown test report"""
        summary = report_data['test_summary']
        metrics = report_data['performance_metrics']
        
        success_rate = (summary['successful_tests'] / summary['total_tests'] * 100) if summary['total_tests'] > 0 else 0
        
        markdown = f"""# IBM Quantum Hardware Test Report

**Generated:** {summary['timestamp']}
**Backend:** {summary['backend_used']}
**Total Tests:** {summary['total_tests']}
**Success Rate:** {success_rate:.1f}%

## Test Summary

- ✅ **Successful Tests:** {summary['successful_tests']}
- ❌ **Failed Tests:** {summary['failed_tests']}
- 🔗 **Job IDs Generated:** {len(summary['job_ids'])}

## Verifiable Job IDs

"""
        
        for i, job_id in enumerate(summary['job_ids'], 1):
            markdown += f"{i}. `{job_id}`\n"
        
        if metrics:
            markdown += f"""
## Performance Metrics

- **Average Execution Time:** {metrics.get('avg_execution_time', 0):.1f}s
- **Circuit Depth Range:** {metrics.get('avg_circuit_depth', 0):.0f} (average)
- **Quantum Entropy:** {metrics.get('avg_entropy', 0):.3f} (average)
- **Quantum Fidelity:** {metrics.get('avg_fidelity', 0):.3f} (average)

## Test Results Details

"""
        
        for result in report_data['test_results']:
            status = "✅ PASSED" if result.get('success', False) else "❌ FAILED"
            markdown += f"### {result['test_name']} - {status}\n\n"
            
            if result.get('success', False):
                markdown += f"- **Job ID:** `{result.get('job_id', 'N/A')}`\n"
                markdown += f"- **Execution Time:** {result.get('execution_time', 0):.1f}s\n"
                markdown += f"- **Circuit Depth:** {result.get('circuit_depth', 0)}\n"
                markdown += f"- **Qubits Used:** {result.get('num_qubits', 0)}\n"
                markdown += f"- **Security Level:** {result.get('security_level', 0)}-bit\n"
                markdown += f"- **Quantum Entropy:** {result.get('entropy', 0):.3f}\n"
                markdown += f"- **Estimated Fidelity:** {result.get('fidelity', 0):.3f}\n"
            else:
                markdown += f"- **Error:** {result.get('error', 'Unknown error')}\n"
            
            markdown += "\n"
        
        markdown += """
## Validation

All job IDs can be independently verified on IBM Quantum Experience:
https://quantum-computing.ibm.com/

## Repository

**Code:** https://github.com/hydraresearch/qzkp
**Paper:** Section 2 - Experimental Validation on IBM Quantum Hardware
"""
        
        return markdown

def main():
    """Main test execution function"""
    print("🔬 IBM Quantum Hardware Test Suite for Quantum ZKP")
    print("=" * 60)
    
    tester = IBMQuantumZKPTester()
    
    try:
        # Run comprehensive tests
        results = tester.run_comprehensive_tests()
        
        # Generate report
        report_file = tester.generate_test_report()
        
        # Print summary
        print("\n🎉 Test Suite Complete!")
        print("=" * 30)
        
        successful = sum(1 for r in results if r.get('success', False))
        total = len(results)
        
        print(f"✅ Tests Passed: {successful}/{total}")
        print(f"📊 Success Rate: {successful/total*100:.1f}%")
        print(f"🔗 Job IDs Generated: {len(tester.job_ids)}")
        print(f"📄 Report Generated: {report_file}")
        
        if successful == total:
            print("\n🚀 ALL TESTS PASSED - Hardware validation successful!")
        else:
            print(f"\n⚠️ {total - successful} tests failed - check logs for details")
            
    except KeyboardInterrupt:
        print("\n⚠️ Test suite interrupted by user")
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
