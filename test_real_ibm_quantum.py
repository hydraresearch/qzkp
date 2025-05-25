#!/usr/bin/env python3
"""
Test with REAL IBM Quantum hardware - using actual quantum time!
⚠️ WARNING: This uses your monthly quantum time allocation!
"""

import os
import sys
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from qiskit import QuantumCircuit, transpile
    from qiskit.quantum_info import Statevector
    from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
    from qiskit.transpiler import generate_preset_pass_manager
    print("✅ Qiskit imports successful")
except ImportError as e:
    print(f"❌ Failed to import Qiskit: {e}")
    sys.exit(1)

def test_real_quantum_hardware():
    """Test with REAL IBM Quantum hardware - uses quantum time!"""
    print("🚀 REAL IBM Quantum Hardware Test")
    print("=" * 40)
    print("⚠️  WARNING: This will use your monthly quantum time!")
    
    api_key = os.getenv('IQKAPI')
    if not api_key:
        print("❌ No API key found")
        return
    
    try:
        # Connect to IBM Quantum with real hardware
        service = QiskitRuntimeService(
            channel='ibm_quantum',
            token=api_key
        )
        
        # Get real quantum backends (not simulators)
        backends = service.backends(simulator=False, operational=True)
        if not backends:
            print("❌ No real quantum backends available")
            return
        
        backend = backends[0]  # Use first available real backend
        print(f"🔗 Using REAL quantum backend: {backend.name}")
        print(f"📊 Backend qubits: {backend.num_qubits}")
        
        # Create a simple Bell state circuit for real execution
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure_all()
        
        print(f"📊 Circuit: {qc.num_qubits} qubits, {qc.depth()} depth")
        
        # Transpile for the real backend
        pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
        transpiled_qc = pm.run(qc)
        
        print(f"📊 Transpiled depth: {transpiled_qc.depth()}")
        print(f"🚀 Submitting job to REAL quantum hardware: {backend.name}")
        
        # Submit job to REAL quantum hardware
        sampler = Sampler(backend)
        job = sampler.run([transpiled_qc], shots=1000)  # Use 1000 shots for good statistics
        
        print(f"📋 Job ID: {job.job_id()}")
        print(f"🔄 Job status: {job.status()}")
        print(f"⏱️  Waiting for REAL quantum execution...")
        
        # Wait for completion
        try:
            result = job.result()
            print(f"✅ REAL quantum job completed successfully!")
            
            # Extract results
            pub_result = result[0]
            counts = pub_result.data.meas.get_counts()
            
            print(f"🎉 REAL Quantum Results from {backend.name}:")
            print(f"📊 Total shots: {sum(counts.values())}")
            
            # Analyze Bell state results
            for bitstring, count in sorted(counts.items()):
                probability = count / sum(counts.values())
                print(f"   |{bitstring}⟩: {count} shots ({probability:.3f})")
            
            # Calculate Bell state fidelity
            bell_states = counts.get('00', 0) + counts.get('11', 0)
            total_shots = sum(counts.values())
            fidelity = bell_states / total_shots
            
            print(f"🎯 Bell state fidelity: {fidelity:.3f}")
            print(f"🌌 Quantum noise effects captured!")
            
            # Save real quantum data
            real_data = {
                "backend": backend.name,
                "job_id": job.job_id(),
                "circuit_depth": transpiled_qc.depth(),
                "shots": total_shots,
                "counts": dict(counts),
                "bell_fidelity": fidelity,
                "timestamp": str(job.creation_date),
                "quantum_hardware": True
            }
            
            with open("real_quantum_results.json", "w") as f:
                json.dump(real_data, f, indent=2)
            
            print(f"💾 Real quantum data saved to real_quantum_results.json")
            print(f"🎉 SUCCESS: Executed on REAL quantum hardware!")
            
            return real_data
            
        except Exception as e:
            print(f"⚠️  Job execution issue: {e}")
            print(f"💡 This can happen with real quantum hardware")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    print("🌌 IBM Quantum REAL Hardware Test")
    print("=" * 35)
    print("⚠️  WARNING: This uses your 10-minute monthly allocation!")
    print("🔄 This test will execute a Bell state on real quantum hardware")
    print("📊 Expected time: 30-120 seconds")
    
    # Ask for confirmation
    response = input("\n❓ Do you want to proceed with REAL quantum hardware? (y/N): ")
    if response.lower() != 'y':
        print("📋 Test cancelled. Use simulator mode instead:")
        print("   python qiskit_executor.py --simulator")
        return
    
    print("\n🚀 Proceeding with REAL quantum hardware execution...")
    
    real_data = test_real_quantum_hardware()
    
    if real_data:
        print(f"\n🎉 REAL Quantum Hardware Test SUCCESSFUL!")
        print(f"✅ Backend: {real_data['backend']}")
        print(f"✅ Job ID: {real_data['job_id']}")
        print(f"✅ Bell fidelity: {real_data['bell_fidelity']:.3f}")
        print(f"✅ Total shots: {real_data['shots']}")
        print(f"✅ Data saved: real_quantum_results.json")
        
        print(f"\n🔬 This data can now be used in your scientific paper!")
        print(f"📄 Real quantum hardware validation complete!")
    else:
        print(f"\n⚠️  Real quantum hardware test encountered issues")
        print(f"💡 This is normal - quantum hardware can be busy or have errors")
        print(f"🔄 Try again later or use simulator mode for development")
    
    print(f"\n💡 Remember: Use simulator mode for development to save quantum time!")

if __name__ == "__main__":
    main()
