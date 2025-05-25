#!/usr/bin/env python3
"""
Simple IBM Quantum authentication test
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

def test_auth_methods():
    """Test different authentication methods"""
    api_key = os.getenv('IQKAPI')
    if not api_key:
        print("❌ No API key found")
        return
    
    print(f"🔑 Testing with API key: {api_key[:10]}...")
    
    # Method 1: Direct token authentication
    try:
        print("\n📋 Method 1: Direct token authentication...")
        service = QiskitRuntimeService(token=api_key)
        backends = service.backends()
        print(f"✅ SUCCESS! Found {len(backends)} backends")
        return service, backends
    except Exception as e:
        print(f"❌ Method 1 failed: {e}")
    
    # Method 2: Save account and load
    try:
        print("\n📋 Method 2: Save account...")
        QiskitRuntimeService.save_account(token=api_key, overwrite=True)
        service = QiskitRuntimeService()
        backends = service.backends()
        print(f"✅ SUCCESS! Found {len(backends)} backends")
        return service, backends
    except Exception as e:
        print(f"❌ Method 2 failed: {e}")
    
    # Method 3: Environment variable
    try:
        print("\n📋 Method 3: Environment variable...")
        os.environ['QISKIT_IBM_TOKEN'] = api_key
        service = QiskitRuntimeService()
        backends = service.backends()
        print(f"✅ SUCCESS! Found {len(backends)} backends")
        return service, backends
    except Exception as e:
        print(f"❌ Method 3 failed: {e}")
    
    return None, None

def main():
    print("🚀 IBM Quantum Simple Authentication Test")
    print("=" * 45)
    
    service, backends = test_auth_methods()
    
    if service and backends:
        print(f"\n🎉 Authentication successful!")
        print(f"📊 Available backends: {len(backends)}")
        
        # List some backends
        print(f"\n🖥️  Sample backends:")
        for i, backend in enumerate(backends[:5]):  # Show first 5
            print(f"   {i+1}. {backend.name}")
        
        if len(backends) > 5:
            print(f"   ... and {len(backends) - 5} more")
            
        print(f"\n✅ Your IBM Quantum integration is working!")
        print(f"💡 You can now generate real quantum states")
        
    else:
        print(f"\n❌ All authentication methods failed")
        print(f"💡 Possible issues:")
        print(f"   1. API key might be incorrect")
        print(f"   2. Account might not be activated")
        print(f"   3. Network connectivity issues")
        print(f"   4. IBM Quantum service might be down")
        
        print(f"\n🔧 Troubleshooting:")
        print(f"   1. Check your API key at: https://quantum.ibm.com/")
        print(f"   2. Verify your account is active")
        print(f"   3. Try again in a few minutes")
        
        print(f"\n📋 For now, you can still use simulator mode:")
        print(f"   python qiskit_executor.py --simulator")

if __name__ == "__main__":
    main()
