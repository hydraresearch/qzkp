#!/bin/bash

# Setup script for IBM Quantum Integration Python Environment
# Creates a Python 3.11 virtual environment with all required dependencies

set -e  # Exit on any error

echo "🚀 Setting up IBM Quantum Integration Environment"
echo "================================================="

# Check if Python 3.11 is available
if command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
    echo "✅ Found Python 3.11"
elif command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    if [[ "$PYTHON_VERSION" == "3.11" ]]; then
        PYTHON_CMD="python3"
        echo "✅ Found Python 3.11 (as python3)"
    else
        echo "⚠️  Warning: Found Python $PYTHON_VERSION, but Python 3.11 is recommended"
        echo "   Continuing with python3..."
        PYTHON_CMD="python3"
    fi
else
    echo "❌ Error: Python 3.11 not found"
    echo "   Please install Python 3.11:"
    echo "   - macOS: brew install python@3.11"
    echo "   - Ubuntu: sudo apt install python3.11 python3.11-venv"
    echo "   - Windows: Download from python.org"
    exit 1
fi

# Create virtual environment
echo ""
echo "📦 Creating virtual environment 'quantum_env'..."
if [ -d "quantum_env" ]; then
    echo "⚠️  Virtual environment 'quantum_env' already exists"
    read -p "   Do you want to recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Removing existing environment..."
        rm -rf quantum_env
    else
        echo "📋 Using existing environment..."
    fi
fi

if [ ! -d "quantum_env" ]; then
    $PYTHON_CMD -m venv quantum_env
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source quantum_env/bin/activate

# Upgrade pip
echo ""
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "📚 Installing Python packages from requirements.txt..."
echo "   This may take a few minutes..."

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ All packages installed successfully"
else
    echo "❌ Error: requirements.txt not found"
    exit 1
fi

# Verify Qiskit installation
echo ""
echo "🧪 Verifying Qiskit installation..."
python -c "
import qiskit
import qiskit_ibm_runtime
import numpy as np
print(f'✅ Qiskit version: {qiskit.__version__}')
print(f'✅ Qiskit IBM Runtime version: {qiskit_ibm_runtime.__version__}')
print(f'✅ NumPy version: {np.__version__}')
print('🎉 All packages imported successfully!')
"

# Test the quantum executor
echo ""
echo "🔬 Testing quantum executor..."
if [ -f "qiskit_executor.py" ]; then
    python qiskit_executor.py --help > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "✅ Quantum executor is working"
    else
        echo "⚠️  Quantum executor test failed (this is normal if dependencies are missing)"
    fi
else
    echo "⚠️  qiskit_executor.py not found"
fi

# Create activation script
echo ""
echo "📝 Creating activation script..."
cat > activate_quantum_env.sh << 'EOF'
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
EOF

chmod +x activate_quantum_env.sh

# Create deactivation reminder
echo ""
echo "🎉 Setup complete!"
echo "=================="
echo ""
echo "📋 Next steps:"
echo "   1. Activate environment: source quantum_env/bin/activate"
echo "   2. Or use shortcut:      ./activate_quantum_env.sh"
echo "   3. Test integration:     python qiskit_executor.py --simulator"
echo "   4. Run Go tests:         go run test_real_quantum_states.go"
echo ""
echo "💡 Tips:"
echo "   - Always activate the environment before running quantum code"
echo "   - Deactivate with: deactivate"
echo "   - Update packages: pip install -r requirements.txt --upgrade"
echo ""
echo "🔑 Don't forget to set your IBM Quantum API key in .env:"
echo "   IQKAPI=your_api_key_here"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating template..."
    cat > .env << 'EOF'
# IBM Quantum API Key
# Get your key from: https://quantum.ibm.com/
IQKAPI=your_ibm_quantum_api_key_here
EOF
    echo "✅ Created .env template - please add your API key"
fi

echo "🌟 IBM Quantum Integration environment is ready!"
