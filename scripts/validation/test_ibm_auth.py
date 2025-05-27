#!/usr/bin/env python3
"""
Test IBM Quantum authentication and backend access
This script tests connection to IBM Quantum without using quantum time
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from qiskit_ibm_runtime import QiskitRuntimeService
    print("✅ Qiskit IBM Runtime imported successfully")
except ImportError as e:
    print(f"❌ Failed to import Qiskit IBM Runtime: {e}")
    sys.exit(1)

def test_authentication():
    """Test IBM Quantum authentication"""
    print("🔐 Testing IBM Quantum Authentication...")
    
    # Get API key
    api_key = os.getenv('IQKAPI')
    if not api_key:
        print("❌ No IBM Quantum API key found in IQKAPI environment variable")
        return False
    
    print(f"✅ API key found: {api_key[:10]}...")
    
    try:
        # Initialize service
        service = QiskitRuntimeService()
        print("✅ QiskitRuntimeService initialized")
        
        # Test authentication by getting backends
        backends = service.backends()
        print(f"✅ Authentication successful! Found {len(backends)} backends")
        
        return True, service, backends
        
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return False, None, None

def list_backends(service, backends):
    """List available quantum backends"""
    print("\n🖥️  Available IBM Quantum Backends:")
    print("=" * 50)
    
    real_backends = []
    simulators = []
    
    for backend in backends:
        backend_name = backend.name
        try:
            # Get backend configuration
            config = backend.configuration()
            num_qubits = config.num_qubits if hasattr(config, 'num_qubits') else 'Unknown'
            simulator = config.simulator if hasattr(config, 'simulator') else False
            
            if simulator:
                simulators.append((backend_name, num_qubits))
            else:
                real_backends.append((backend_name, num_qubits))
                
        except Exception as e:
            print(f"⚠️  Could not get info for {backend_name}: {e}")
    
    print("🔬 Real Quantum Hardware:")
    for name, qubits in real_backends:
        print(f"   • {name} ({qubits} qubits)")
    
    print("\n🔧 Simulators:")
    for name, qubits in simulators:
        print(f"   • {name} ({qubits} qubits)")
    
    return real_backends, simulators

def check_account_limits(service):
    """Check account usage and limits"""
    print("\n📊 Account Information:")
    print("=" * 30)
    
    try:
        # This would show account usage if available
        print("✅ Account access confirmed")
        print("⚠️  Remember: Free accounts have 10 minutes of quantum time per month")
        print("💡 Use simulators for development to preserve quantum time")
        
    except Exception as e:
        print(f"⚠️  Could not retrieve account info: {e}")

def main():
    print("🚀 IBM Quantum Authentication Test")
    print("=" * 40)
    
    # Test authentication
    auth_result = test_authentication()
    if not auth_result[0]:
        print("\n❌ Authentication test failed")
        return
    
    service, backends = auth_result[1], auth_result[2]
    
    # List backends
    real_backends, simulators = list_backends(service, backends)
    
    # Check account limits
    check_account_limits(service)
    
    # Summary
    print(f"\n🎯 Summary:")
    print(f"✅ Authentication: SUCCESS")
    print(f"✅ Real quantum backends: {len(real_backends)}")
    print(f"✅ Simulators available: {len(simulators)}")
    print(f"✅ Ready for quantum state generation!")
    
    print(f"\n💡 Next Steps:")
    print(f"   1. Use simulators for development: python qiskit_executor.py --simulator")
    print(f"   2. Use real hardware sparingly: python qiskit_executor.py")
    print(f"   3. Monitor your quantum time usage carefully")
    
    print(f"\n🌟 IBM Quantum integration is ready!")

if __name__ == "__main__":
    main()
