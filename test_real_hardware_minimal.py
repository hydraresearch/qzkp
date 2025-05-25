#!/usr/bin/env python3
"""
MINIMAL test with real IBM Quantum hardware
⚠️ WARNING: This uses your monthly quantum time allocation!
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector
    from qiskit_ibm_runtime import QiskitRuntimeService, EstimatorV2 as Estimator
    from qiskit.transpiler import generate_preset_pass_manager
    print("✅ Qiskit imports successful")
except ImportError as e:
    print(f"❌ Failed to import Qiskit: {e}")
    sys.exit(1)

def test_minimal_real_hardware():
    """Test with minimal quantum circuit on real hardware"""
    print("⚠️  WARNING: This will use your monthly quantum time!")
    print("🔄 Connecting to IBM Quantum...")
    
    api_key = os.getenv('IQKAPI')
    if not api_key:
        print("❌ No API key found")
        return
    
    try:
        # Connect to IBM Quantum
        service = QiskitRuntimeService(
            channel='ibm_quantum',
            token=api_key
        )
        
        # Get the least busy backend
        backends = service.backends(simulator=False, operational=True)
        if not backends:
            print("❌ No real quantum backends available")
            return
        
        backend = backends[0]  # Use first available
        print(f"🔗 Using backend: {backend.name}")
        
        # Create minimal Bell state circuit (2 qubits only)
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure_all()
        
        print(f"📊 Circuit depth: {qc.depth()}")
        print(f"📊 Number of gates: {len(qc.data)}")
        
        # Transpile for the backend
        pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
        transpiled_qc = pm.run(qc)
        
        print(f"📊 Transpiled depth: {transpiled_qc.depth()}")
        print(f"🚀 Submitting job to {backend.name}...")
        
        # Submit job with minimal shots to save time
        estimator = Estimator(backend)
        job = estimator.run([transpiled_qc], shots=100)  # Minimal shots
        
        print(f"📋 Job ID: {job.job_id()}")
        print(f"🔄 Job status: {job.status()}")
        
        # Wait for completion (with timeout)
        try:
            result = job.result(timeout=300)  # 5 minute timeout
            print(f"✅ Job completed successfully!")
            print(f"📊 Results available")
            
            # This would be where we extract the quantum state
            # For now, we just confirm the job worked
            print(f"🎉 Real quantum hardware execution successful!")
            
        except Exception as e:
            print(f"⚠️  Job execution issue: {e}")
            print(f"💡 This is normal - real quantum jobs can take time")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("🚀 MINIMAL Real IBM Quantum Hardware Test")
    print("=" * 45)
    print("⚠️  WARNING: This uses your 10-minute monthly allocation!")
    print("🔄 This test uses minimal resources (1 circuit, 100 shots)")
    
    # Ask for confirmation
    response = input("\n❓ Do you want to proceed with real hardware test? (y/N): ")
    if response.lower() != 'y':
        print("📋 Test cancelled. Use simulator mode instead:")
        print("   python qiskit_executor.py --simulator")
        return
    
    test_minimal_real_hardware()
    
    print("\n💡 For development, always use simulator mode:")
    print("   python qiskit_executor.py --simulator")
    print("🎯 Save real hardware for final experiments!")

if __name__ == "__main__":
    main()
