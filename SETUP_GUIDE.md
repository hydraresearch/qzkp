# 🚀 IBM Quantum Integration Setup Guide

This guide will help you set up a Python 3.11 virtual environment with all the necessary dependencies for IBM Quantum integration.

## 📋 Prerequisites

### 1. Python 3.11
Install Python 3.11 on your system:

**macOS (using Homebrew):**
```bash
brew install python@3.11
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-pip
```

**Windows:**
Download from [python.org](https://www.python.org/downloads/) and install Python 3.11

### 2. IBM Quantum Account
- Sign up at [IBM Quantum](https://quantum.ibm.com/)
- Get your API key from the dashboard
- **Important**: Free accounts have 10 minutes of quantum time per month

## 🔧 Quick Setup (Automated)

### Option 1: Run the Setup Script
```bash
./setup_quantum_env.sh
```

This script will:
- ✅ Check for Python 3.11
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Verify installation
- ✅ Create activation scripts

### Option 2: Manual Setup

If you prefer manual setup or the script doesn't work:

```bash
# 1. Create virtual environment with Python 3.11
python3.11 -m venv quantum_env

# 2. Activate the environment
source quantum_env/bin/activate

# 3. Upgrade pip
pip install --upgrade pip

# 4. Install dependencies
pip install -r requirements.txt

# 5. Verify installation
python test_python_setup.py
```

## 🔑 Configure API Key

### 1. Create/Edit .env file
```bash
# Create .env file with your IBM Quantum API key
echo "IQKAPI=your_actual_api_key_here" > .env
```

### 2. Get Your API Key
1. Go to [IBM Quantum](https://quantum.ibm.com/)
2. Sign in to your account
3. Navigate to your account settings
4. Copy your API key
5. Replace `your_actual_api_key_here` in `.env`

## 🧪 Test Your Setup

### 1. Test Python Environment
```bash
# Activate environment
source quantum_env/bin/activate

# Run comprehensive test
python test_python_setup.py
```

Expected output:
```
🧪 IBM Quantum Integration - Python Environment Test
=======================================================
🐍 Testing Python version...
✅ Python version is compatible

📦 Testing package imports...
✅ NumPy: 1.24.3
✅ Qiskit: 2.0.0
✅ Qiskit IBM Runtime: 0.37.0
✅ Matplotlib: 3.7.1
✅ python-dotenv: 1.0.0

🔬 Testing Qiskit functionality...
✅ Created Bell state circuit with 2 qubits
✅ Generated statevector with 4 amplitudes

🔑 Testing environment variables...
✅ IQKAPI found: eab083f7af...

🚀 Testing quantum executor...
✅ qiskit_executor.py imports successfully
✅ QuantumStateGenerator created successfully
✅ Bell state circuit created with 2 qubits

🎯 Results: 5/5 tests passed
🎉 All tests passed! Your environment is ready!
```

### 2. Test Quantum State Generation
```bash
# Test with simulator (doesn't use quantum time)
python qiskit_executor.py --simulator

# Test with real hardware (uses quantum time!)
python qiskit_executor.py
```

### 3. Test Go Integration
```bash
# Make sure Go can find the Python environment
go run test_real_quantum_states.go
```

## 📁 File Structure

After setup, you should have:
```
quantumzkp/
├── quantum_env/              # Python virtual environment
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (API key)
├── setup_quantum_env.sh      # Setup script
├── activate_quantum_env.sh   # Quick activation script
├── test_python_setup.py      # Environment test script
├── qiskit_executor.py        # Python-Qiskit bridge
├── ibm_quantum.go           # Go IBM Quantum client
├── quantum_state_cache.go   # Caching system
└── test_real_quantum_states.go # Integration demo
```

## 🔄 Daily Usage

### Activate Environment
```bash
# Method 1: Direct activation
source quantum_env/bin/activate

# Method 2: Use convenience script
./activate_quantum_env.sh
```

### Deactivate Environment
```bash
deactivate
```

### Update Dependencies
```bash
source quantum_env/bin/activate
pip install -r requirements.txt --upgrade
```

## 🛠️ Troubleshooting

### Common Issues

**1. Python 3.11 not found**
```bash
# Check available Python versions
ls /usr/bin/python*
which python3.11

# Install Python 3.11 (see prerequisites above)
```

**2. Virtual environment creation fails**
```bash
# Install venv module
sudo apt install python3.11-venv  # Ubuntu
brew install python@3.11          # macOS
```

**3. Qiskit installation fails**
```bash
# Update pip first
pip install --upgrade pip setuptools wheel

# Install with verbose output
pip install -v qiskit[all]
```

**4. IBM Quantum authentication fails**
```bash
# Check API key
echo $IQKAPI
cat .env

# Test authentication
python -c "
import os
from qiskit_ibm_runtime import QiskitRuntimeService
service = QiskitRuntimeService()
print('Authentication successful!')
"
```

**5. Go can't find Python script**
```bash
# Make sure you're in the right directory
pwd
ls qiskit_executor.py

# Check Python path in activated environment
which python
```

### Debug Mode

Enable verbose logging:
```bash
export QUANTUM_DEBUG=1
python test_python_setup.py
```

## 📊 Resource Management

### Monitor Quantum Time Usage
```bash
# Check usage in Go
go run -c "
ibm, _ := NewIBMQuantumClient()
stats, _ := ibm.Cache.GetUsageStats()
fmt.Printf('Used time: %.2f seconds\n', stats.UsedTimeSeconds)
"
```

### Use Simulator for Development
```bash
# Always use --simulator flag during development
python qiskit_executor.py --simulator

# Only use real hardware for final testing
python qiskit_executor.py  # Uses real quantum time!
```

## 🎯 Next Steps

Once setup is complete:

1. **Test the integration**: `go run test_real_quantum_states.go`
2. **Run your existing tests**: Your ZKP tests now use real quantum data
3. **Explore quantum states**: Check the generated cache files
4. **Update your research**: Use real quantum data in your papers

## 📚 Additional Resources

- [IBM Quantum Documentation](https://docs.quantum.ibm.com/)
- [Qiskit Tutorials](https://qiskit.org/documentation/tutorials/)
- [IBM Quantum Network](https://quantum.ibm.com/network)

---

**⚠️ Important**: Always use simulator mode during development to preserve your monthly quantum time allocation for important experiments!
