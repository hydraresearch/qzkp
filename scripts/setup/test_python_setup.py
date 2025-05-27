#!/usr/bin/env python3
"""
Test script to verify Python environment setup for IBM Quantum integration
"""

import sys
import os

def test_python_version():
    """Test Python version"""
    print("🐍 Testing Python version...")
    version = sys.version_info
    print(f"   Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 11:
        print("✅ Python version is compatible")
        return True
    else:
        print("⚠️  Python 3.11+ recommended for best compatibility")
        return True  # Still allow other versions

def test_imports():
    """Test required package imports"""
    print("\n📦 Testing package imports...")
    
    packages = [
        ("numpy", "NumPy"),
        ("qiskit", "Qiskit"),
        ("qiskit_ibm_runtime", "Qiskit IBM Runtime"),
        ("matplotlib", "Matplotlib"),
        ("dotenv", "python-dotenv"),
    ]
    
    success_count = 0
    for package, name in packages:
        try:
            module = __import__(package)
            version = getattr(module, '__version__', 'unknown')
            print(f"✅ {name}: {version}")
            success_count += 1
        except ImportError as e:
            print(f"❌ {name}: Not installed ({e})")
    
    print(f"\n📊 Import results: {success_count}/{len(packages)} packages available")
    return success_count == len(packages)

def test_qiskit_functionality():
    """Test basic Qiskit functionality"""
    print("\n🔬 Testing Qiskit functionality...")
    
    try:
        from qiskit import QuantumCircuit
        from qiskit.quantum_info import Statevector
        
        # Create a simple Bell state circuit
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        
        # Get statevector
        state = Statevector.from_instruction(qc)
        
        print(f"✅ Created Bell state circuit with {qc.num_qubits} qubits")
        print(f"✅ Generated statevector with {len(state.data)} amplitudes")
        print(f"   First amplitude: {state.data[0]:.3f}")
        print(f"   Last amplitude: {state.data[-1]:.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Qiskit functionality test failed: {e}")
        return False

def test_environment_variables():
    """Test environment variable loading"""
    print("\n🔑 Testing environment variables...")
    
    # Test .env file loading
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ python-dotenv loaded successfully")
    except ImportError:
        print("⚠️  python-dotenv not available")
    
    # Check for IBM Quantum API key
    api_key = os.getenv('IQKAPI')
    if api_key:
        if api_key == "your_ibm_quantum_api_key_here":
            print("⚠️  IQKAPI found but appears to be template value")
            print("   Please update .env with your real IBM Quantum API key")
        else:
            print(f"✅ IQKAPI found: {api_key[:10]}...")
    else:
        print("⚠️  IQKAPI not found in environment variables")
        print("   Add your IBM Quantum API key to .env file")
    
    return True

def test_quantum_executor():
    """Test the quantum executor script"""
    print("\n🚀 Testing quantum executor...")
    
    if not os.path.exists('qiskit_executor.py'):
        print("❌ qiskit_executor.py not found")
        return False
    
    try:
        # Import the quantum executor module
        sys.path.insert(0, '.')
        import qiskit_executor
        
        print("✅ qiskit_executor.py imports successfully")
        
        # Test creating a quantum state generator
        generator = qiskit_executor.QuantumStateGenerator(use_simulator=True)
        print("✅ QuantumStateGenerator created successfully")
        
        # Test creating a simple circuit
        bell_circuit = generator.create_bell_state()
        print(f"✅ Bell state circuit created with {bell_circuit.num_qubits} qubits")
        
        return True
        
    except Exception as e:
        print(f"❌ Quantum executor test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 IBM Quantum Integration - Python Environment Test")
    print("=" * 55)
    
    tests = [
        ("Python Version", test_python_version),
        ("Package Imports", test_imports),
        ("Qiskit Functionality", test_qiskit_functionality),
        ("Environment Variables", test_environment_variables),
        ("Quantum Executor", test_quantum_executor),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 55)
    print("📊 Test Summary:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Your environment is ready for IBM Quantum integration.")
        print("\n📋 Next steps:")
        print("   1. Set your IBM Quantum API key in .env")
        print("   2. Run: python qiskit_executor.py --simulator")
        print("   3. Run: go run test_real_quantum_states.go")
    else:
        print("\n⚠️  Some tests failed. Please check the setup:")
        print("   1. Run: ./setup_quantum_env.sh")
        print("   2. Activate environment: source quantum_env/bin/activate")
        print("   3. Install packages: pip install -r requirements.txt")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
