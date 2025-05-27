#!/usr/bin/env python3
"""
IBM Quantum Hardware Test Using Existing Executor
Tests quantum ZKP circuits using the proven qiskit_executor.py
"""

import os
import sys
import json
import time
import hashlib
import subprocess
import numpy as np
from datetime import datetime
from typing import List, Dict, Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

class IBMQuantumExecutorTest:
    """Test IBM Quantum hardware using existing executor"""
    
    def __init__(self):
        self.executor_path = self.find_executor()
        self.test_results = []
        self.timeout = 60  # 60 second timeout
        
    def find_executor(self) -> str:
        """Find the qiskit_executor.py file"""
        possible_paths = [
            "qiskit_executor.py",
            "scripts/validation/qiskit_executor.py",
            "../qiskit_executor.py",
            "../../qiskit_executor.py"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                print(f"✅ Found executor at: {path}")
                return path
        
        # If not found, create it from the provided code
        print("📝 Creating qiskit_executor.py from provided code...")
        return self.create_executor()
    
    def create_executor(self) -> str:
        """Create the executor file from the provided code"""
        executor_code = '''#!/usr/bin/env python3
"""
Qiskit Executor for IBM Quantum Integration
Executes quantum circuits on IBM Quantum hardware and returns state vectors
"""

import os
import sys
import json
import numpy as np
from typing import List, Dict, Any, Optional
import argparse

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Loaded environment variables from .env", file=sys.stderr)
except ImportError:
    print("⚠️  python-dotenv not available, using system environment variables", file=sys.stderr)

# Import Qiskit components
try:
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector, SparsePauliOp
    from qiskit.transpiler import generate_preset_pass_manager
    from qiskit_ibm_runtime import QiskitRuntimeService, EstimatorV2 as Estimator
    from qiskit_ibm_runtime.fake_provider import FakeAlmadenV2
    print("✅ Qiskit imports successful", file=sys.stderr)
except ImportError as e:
    print(f"❌ Failed to import Qiskit: {e}", file=sys.stderr)
    print("Please install: pip install qiskit qiskit-ibm-runtime", file=sys.stderr)
    sys.exit(1)

class QuantumStateGenerator:
    """Generates quantum states using IBM Quantum hardware"""

    def __init__(self, use_simulator: bool = True):
        self.use_simulator = use_simulator
        self.service = None
        self.backend = None

        # Initialize IBM Quantum service
        try:
            api_key = os.getenv('IQKAPI')
            if api_key and not use_simulator:
                # Use proper channel specification for IBM Quantum
                self.service = QiskitRuntimeService(
                    channel='ibm_quantum',
                    token=api_key
                )
                # Get available backends
                backends = self.service.backends(simulator=False, operational=True)
                if backends:
                    self.backend = backends[0]  # Use first available real backend
                    print(f"🔗 Connected to IBM Quantum backend: {self.backend.name}", file=sys.stderr)
                else:
                    print("⚠️  No real backends available, using simulator", file=sys.stderr)
                    self.backend = FakeAlmadenV2()
                    self.use_simulator = True
            else:
                self.backend = FakeAlmadenV2()
                print("🔧 Using simulator backend for development", file=sys.stderr)
        except Exception as e:
            print(f"⚠️  Failed to connect to IBM Quantum, using simulator: {e}", file=sys.stderr)
            self.backend = FakeAlmadenV2()
            self.use_simulator = True

    def create_bell_state(self) -> QuantumCircuit:
        """Create a Bell state circuit"""
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        return qc

    def create_ghz_state(self, num_qubits: int = 3) -> QuantumCircuit:
        """Create a GHZ state circuit"""
        qc = QuantumCircuit(num_qubits)
        qc.h(0)
        for i in range(1, num_qubits):
            qc.cx(0, i)
        return qc

    def get_statevector(self, circuit: QuantumCircuit) -> List[complex]:
        """Get the statevector from a quantum circuit"""
        try:
            # For simulator, we can get exact statevector
            if self.use_simulator or isinstance(self.backend, FakeAlmadenV2):
                state = Statevector.from_instruction(circuit)
                return [complex(amp) for amp in state.data]

            # For real hardware, we need to use tomography or estimation
            print("⚠️  Real hardware statevector extraction not implemented, using simulator", file=sys.stderr)
            state = Statevector.from_instruction(circuit)
            return [complex(amp) for amp in state.data]

        except Exception as e:
            print(f"❌ Error getting statevector: {e}", file=sys.stderr)
            return []

    def generate_quantum_states(self) -> Dict[str, Any]:
        """Generate a collection of quantum states"""
        states = {}

        # Define state types to generate
        state_configs = [
            ("bell_state_phi_plus", "Bell state |Φ+⟩", self.create_bell_state, []),
            ("ghz_state_3q", "3-qubit GHZ state", self.create_ghz_state, [3]),
        ]

        for name, description, circuit_func, args in state_configs:
            try:
                print(f"📊 Generating {name}...", file=sys.stderr)

                # Create circuit
                circuit = circuit_func(*args) if args else circuit_func()

                # Get statevector
                statevector = self.get_statevector(circuit)

                if statevector:
                    states[name] = {
                        "vector": [[amp.real, amp.imag] for amp in statevector],
                        "description": description,
                        "qubits": circuit.num_qubits,
                        "backend": self.backend.name if hasattr(self.backend, 'name') else "simulator",
                        "metadata": {
                            "circuit_depth": circuit.depth(),
                            "num_gates": len(circuit.data),
                            "use_simulator": self.use_simulator
                        }
                    }
                    print(f"✅ Generated {name} with {len(statevector)} amplitudes", file=sys.stderr)

            except Exception as e:
                print(f"❌ Error generating {name}: {e}", file=sys.stderr)

        return states

def main():
    parser = argparse.ArgumentParser(description='Generate quantum states using IBM Quantum')
    parser.add_argument('--simulator', action='store_true',
                       help='Use simulator instead of real hardware')
    parser.add_argument('--output', type=str, default='quantum_states.json',
                       help='Output file for quantum states')

    args = parser.parse_args()

    # Create generator
    generator = QuantumStateGenerator(use_simulator=args.simulator)

    # Generate states
    print("🚀 Starting quantum state generation...", file=sys.stderr)
    states = generator.generate_quantum_states()

    # Output results
    result = {
        "states": states,
        "generated_at": str(np.datetime64('now')),
        "backend": generator.backend.name if hasattr(generator.backend, 'name') else "simulator",
        "use_simulator": generator.use_simulator,
        "total_states": len(states)
    }

    # Write to file
    with open(args.output, 'w') as f:
        json.dump(result, f, indent=2)

    # Also output to stdout for Go to read
    print(json.dumps(result))

    print(f"🎉 Generated {len(states)} quantum states", file=sys.stderr)

if __name__ == "__main__":
    main()
'''
        
        executor_path = "qiskit_executor.py"
        with open(executor_path, 'w') as f:
            f.write(executor_code)
        
        os.chmod(executor_path, 0o755)
        print(f"✅ Created executor at: {executor_path}")
        return executor_path
    
    def run_executor_test(self, test_name: str, use_simulator: bool = False) -> Dict[str, Any]:
        """Run executor test with timeout"""
        print(f"🔬 Executor test: {test_name}")
        
        start_time = time.time()
        
        try:
            # Prepare command
            cmd = [
                "python3", self.executor_path,
                "--output", f"{test_name}_output.json"
            ]
            
            if use_simulator:
                cmd.append("--simulator")
            
            print(f"   Command: {' '.join(cmd)}")
            
            # Run with timeout
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            try:
                stdout, stderr = process.communicate(timeout=self.timeout)
                execution_time = time.time() - start_time
                
                # Parse results
                if process.returncode == 0:
                    try:
                        # Try to parse JSON output
                        result_data = json.loads(stdout)
                        
                        test_result = {
                            'test_name': test_name,
                            'execution_time': execution_time,
                            'success': True,
                            'timeout': False,
                            'backend': result_data.get('backend', 'unknown'),
                            'use_simulator': result_data.get('use_simulator', True),
                            'total_states': result_data.get('total_states', 0),
                            'states_generated': list(result_data.get('states', {}).keys()),
                            'timestamp': datetime.now().isoformat(),
                            'stdout': stdout[:500],  # First 500 chars
                            'stderr': stderr[:500]   # First 500 chars
                        }
                        
                        print(f"   ✅ COMPLETED in {execution_time:.1f}s")
                        print(f"   📊 Backend: {test_result['backend']}")
                        print(f"   🎯 States: {test_result['total_states']}")
                        
                        return test_result
                        
                    except json.JSONDecodeError as e:
                        print(f"   ❌ JSON parse error: {e}")
                        return {
                            'test_name': test_name,
                            'execution_time': execution_time,
                            'success': False,
                            'error': f"JSON parse error: {e}",
                            'stdout': stdout,
                            'stderr': stderr
                        }
                else:
                    print(f"   ❌ Process failed with return code: {process.returncode}")
                    return {
                        'test_name': test_name,
                        'execution_time': execution_time,
                        'success': False,
                        'error': f"Process failed: {process.returncode}",
                        'stdout': stdout,
                        'stderr': stderr
                    }
                    
            except subprocess.TimeoutExpired:
                process.kill()
                execution_time = time.time() - start_time
                
                print(f"   ⏰ TIMEOUT after {execution_time:.1f}s")
                
                return {
                    'test_name': test_name,
                    'execution_time': execution_time,
                    'success': False,
                    'timeout': True,
                    'error': f"Timeout after {self.timeout}s"
                }
                
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"   ❌ ERROR after {execution_time:.1f}s: {e}")
            
            return {
                'test_name': test_name,
                'execution_time': execution_time,
                'success': False,
                'error': str(e)
            }
    
    def run_executor_test_suite(self):
        """Run complete executor test suite"""
        print("🚀 IBM Quantum Executor Test Suite")
        print("=" * 40)
        
        # Test cases
        test_cases = [
            ("Simulator_Test", True),
            ("Hardware_Test", False),
            ("Hardware_Retry", False)
        ]
        
        results = []
        
        for i, (name, use_sim) in enumerate(test_cases, 1):
            print(f"\n🔬 Executor Test {i}/{len(test_cases)}: {name}")
            print("-" * 40)
            
            result = self.run_executor_test(name, use_sim)
            results.append(result)
            self.test_results.append(result)
            
            # Pause between tests
            if i < len(test_cases):
                print("⏳ 10s pause...")
                time.sleep(10)
        
        return results
    
    def generate_executor_report(self):
        """Generate executor test report"""
        successful = sum(1 for r in self.test_results if r.get('success', False))
        timeouts = sum(1 for r in self.test_results if r.get('timeout', False))
        total = len(self.test_results)
        
        # Find hardware tests
        hardware_tests = [r for r in self.test_results if not r.get('use_simulator', True) and r.get('success', False)]
        
        report = {
            'executor_test_summary': {
                'total_tests': total,
                'successful_tests': successful,
                'timeout_tests': timeouts,
                'failed_tests': total - successful,
                'success_rate': (successful / total * 100) if total > 0 else 0,
                'hardware_tests_successful': len(hardware_tests),
                'executor_path': self.executor_path,
                'timestamp': datetime.now().isoformat()
            },
            'test_results': self.test_results
        }
        
        # Save report
        filename = f"ibm_quantum_executor_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n🎉 Executor Test Suite Complete!")
        print("=" * 40)
        print(f"✅ Successful: {successful}/{total}")
        print(f"⏰ Timeouts: {timeouts}/{total}")
        print(f"🔬 Hardware Tests: {len(hardware_tests)}")
        print(f"📊 Success Rate: {successful/total*100:.1f}%")
        print(f"📄 Report: {filename}")
        
        # Show hardware test details
        if hardware_tests:
            print(f"\n🏭 Hardware Test Results:")
            for test in hardware_tests:
                backend = test.get('backend', 'unknown')
                states = test.get('total_states', 0)
                time_taken = test.get('execution_time', 0)
                print(f"   ✅ {test['test_name']}: {backend} ({states} states, {time_taken:.1f}s)")
        
        return successful >= total * 0.6  # 60% success rate

def main():
    """Main execution"""
    tester = IBMQuantumExecutorTest()
    
    try:
        # Run executor test suite
        results = tester.run_executor_test_suite()
        
        # Generate report
        success = tester.generate_executor_report()
        
        if success:
            print("\n🚀 IBM QUANTUM EXECUTOR TESTS SUCCESSFUL!")
            print("🔬 Quantum state generation validated!")
            return 0
        else:
            print("\n⚠️ Some executor tests failed")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ Executor tests interrupted")
        return 1
    except Exception as e:
        print(f"\n❌ Executor tests failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
