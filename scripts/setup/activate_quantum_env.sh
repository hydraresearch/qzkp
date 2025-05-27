#!/bin/bash
# Activation script for IBM Quantum Integration Environment

echo "🌌 Activating IBM Quantum Environment..."
source quantum_env/bin/activate

echo "✅ Environment activated!"
echo "   Python: $(which python)"
echo "   Qiskit: $(python -c 'import qiskit; print(qiskit.__version__)')"
echo ""
echo "🚀 Ready for quantum computing!"
echo "   Run: python qiskit_executor.py --help"
echo "   Or:  go run test_real_quantum_states.go"
echo ""
