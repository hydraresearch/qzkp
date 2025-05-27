#!/usr/bin/env python3
"""
Fixed IBM Quantum authentication test with proper channel specification
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from qiskit_ibm_runtime import QiskitRuntimeService
    print("✅ Qiskit IBM Runtime imported successfully")
except ImportError as e:
    print(f"❌ Failed to import Qiskit IBM Runtime: {e}")
    exit(1)

def test_auth_with_channel():
    """Test authentication with proper channel specification"""
    api_key = os.getenv('IQKAPI')
    if not api_key:
        print("❌ No API key found")
        return None, None
    
    print(f"🔑 Testing with API key: {api_key[:10]}...")
    
    # Method 1: IBM Quantum channel with token
    try:
        print("\n📋 Method 1: IBM Quantum channel with token...")
        service = QiskitRuntimeService(
            channel='ibm_quantum',
            token=api_key
        )
        backends = service.backends()
        print(f"✅ SUCCESS! Found {len(backends)} backends")
        return service, backends
    except Exception as e:
        print(f"❌ Method 1 failed: {e}")
    
    # Method 2: Save account with channel
    try:
        print("\n📋 Method 2: Save account with channel...")
        QiskitRuntimeService.save_account(
            channel='ibm_quantum',
            token=api_key,
            overwrite=True
        )
        service = QiskitRuntimeService()
        backends = service.backends()
        print(f"✅ SUCCESS! Found {len(backends)} backends")
        return service, backends
    except Exception as e:
        print(f"❌ Method 2 failed: {e}")
    
    # Method 3: IBM Cloud channel (alternative)
    try:
        print("\n📋 Method 3: IBM Cloud channel...")
        service = QiskitRuntimeService(
            channel='ibm_cloud',
            token=api_key
        )
        backends = service.backends()
        print(f"✅ SUCCESS! Found {len(backends)} backends")
        return service, backends
    except Exception as e:
        print(f"❌ Method 3 failed: {e}")
    
    return None, None

def list_backend_details(service, backends):
    """List detailed backend information"""
    print(f"\n🖥️  Backend Details:")
    print("=" * 50)
    
    real_backends = []
    simulators = []
    
    for backend in backends:
        try:
            name = backend.name
            # Try to get configuration
            try:
                config = backend.configuration()
                num_qubits = getattr(config, 'num_qubits', 'Unknown')
                simulator = getattr(config, 'simulator', False)
            except:
                # Fallback if configuration is not available
                num_qubits = 'Unknown'
                simulator = 'simulator' in name.lower() or 'fake' in name.lower()
            
            if simulator:
                simulators.append((name, num_qubits))
            else:
                real_backends.append((name, num_qubits))
                
        except Exception as e:
            print(f"⚠️  Could not get info for backend: {e}")
    
    if real_backends:
        print("🔬 Real Quantum Hardware:")
        for name, qubits in real_backends:
            print(f"   • {name} ({qubits} qubits)")
    else:
        print("🔬 No real quantum hardware found (might be access level)")
    
    if simulators:
        print(f"\n🔧 Simulators:")
        for name, qubits in simulators:
            print(f"   • {name} ({qubits} qubits)")
    
    return real_backends, simulators

def main():
    print("🚀 IBM Quantum Fixed Authentication Test")
    print("=" * 45)
    
    service, backends = test_auth_with_channel()
    
    if service and backends:
        print(f"\n🎉 Authentication successful!")
        print(f"📊 Total backends available: {len(backends)}")
        
        # List backend details
        real_backends, simulators = list_backend_details(service, backends)
        
        print(f"\n📋 Account Summary:")
        print(f"   ✅ Authentication: SUCCESS")
        print(f"   🔬 Real quantum backends: {len(real_backends)}")
        print(f"   🔧 Simulators: {len(simulators)}")
        
        print(f"\n💡 Usage Recommendations:")
        if real_backends:
            print(f"   🎯 You have access to real quantum hardware!")
            print(f"   ⚠️  Remember: 10 minutes of quantum time per month")
            print(f"   🔧 Use simulators for development")
            print(f"   🚀 Use real hardware for final experiments")
        else:
            print(f"   🔧 Currently showing simulators only")
            print(f"   💡 Real hardware access may require account upgrade")
        
        print(f"\n🚀 Ready to generate quantum states!")
        print(f"   Simulator: python qiskit_executor.py --simulator")
        if real_backends:
            print(f"   Real HW:   python qiskit_executor.py")
        
    else:
        print(f"\n❌ Authentication failed with all methods")
        print(f"\n🔧 Possible solutions:")
        print(f"   1. Verify API key at: https://quantum.ibm.com/")
        print(f"   2. Check if account is properly activated")
        print(f"   3. Ensure you have IBM Quantum Network access")
        print(f"   4. Try regenerating your API key")
        
        print(f"\n📋 You can still use the integration in simulator mode:")
        print(f"   python qiskit_executor.py --simulator")
        print(f"   This provides realistic quantum states for development!")

if __name__ == "__main__":
    main()
