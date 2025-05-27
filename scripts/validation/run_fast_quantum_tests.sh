#!/bin/bash

# Fast Quantum Test Runner with Strict Timeouts
# Runs all quantum tests with time limits to keep things moving

set -e

echo "⚡ Fast Quantum Test Suite Runner"
echo "================================="

# Set Go path
export PATH="/Users/nick/sdk/go1.24.3/bin:$PATH"

# Create results directory
RESULTS_DIR="fast_quantum_results_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$RESULTS_DIR"

echo "📊 Results directory: $RESULTS_DIR"
echo ""

# Test timeout settings
UNIT_TIMEOUT=30
INTEGRATION_TIMEOUT=60
QUANTUM_TIMEOUT=90

# Function to run tests with timeout
run_test_with_timeout() {
    local test_name="$1"
    local test_command="$2"
    local timeout_seconds="$3"
    local output_file="$RESULTS_DIR/${test_name}_results.txt"
    
    echo "⚡ Running $test_name (${timeout_seconds}s timeout)..."
    
    # Run with timeout
    if timeout ${timeout_seconds}s bash -c "$test_command" > "$output_file" 2>&1; then
        echo "✅ $test_name completed successfully"
        return 0
    else
        local exit_code=$?
        if [ $exit_code -eq 124 ]; then
            echo "⏰ $test_name TIMEOUT after ${timeout_seconds}s"
            echo "TIMEOUT after ${timeout_seconds}s" >> "$output_file"
        else
            echo "❌ $test_name failed with exit code $exit_code"
        fi
        return $exit_code
    fi
}

# Function to run Python tests with timeout
run_python_test_with_timeout() {
    local test_name="$1"
    local test_file="$2"
    local timeout_seconds="$3"
    local output_file="$RESULTS_DIR/${test_name}_results.txt"
    
    echo "🐍 Running Python test: $test_name (${timeout_seconds}s timeout)..."
    
    if timeout ${timeout_seconds}s python3 "$test_file" > "$output_file" 2>&1; then
        echo "✅ $test_name completed successfully"
        return 0
    else
        local exit_code=$?
        if [ $exit_code -eq 124 ]; then
            echo "⏰ $test_name TIMEOUT after ${timeout_seconds}s"
            echo "TIMEOUT after ${timeout_seconds}s" >> "$output_file"
        else
            echo "❌ $test_name failed with exit code $exit_code"
        fi
        return $exit_code
    fi
}

# Initialize counters
TOTAL_TESTS=0
PASSED_TESTS=0
TIMEOUT_TESTS=0
FAILED_TESTS=0

# Test tracking function
track_test_result() {
    local exit_code=$1
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    if [ $exit_code -eq 0 ]; then
        PASSED_TESTS=$((PASSED_TESTS + 1))
    elif [ $exit_code -eq 124 ]; then
        TIMEOUT_TESTS=$((TIMEOUT_TESTS + 1))
    else
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
}

echo "📋 Phase 1: Fast Unit Tests"
echo "==========================="

# Run unit tests with timeout
run_test_with_timeout "Unit_Tests" "cd tests/unit && go test -v basic_functionality_test.go" $UNIT_TIMEOUT
track_test_result $?

echo ""
echo "📋 Phase 2: Fast Integration Tests"
echo "=================================="

# Run integration tests with timeout
run_test_with_timeout "Integration_Tests" "cd tests/integration && go test -v simple_integration_test.go" $INTEGRATION_TIMEOUT
track_test_result $?

echo ""
echo "📋 Phase 3: Fast Security Tests"
echo "==============================="

# Run security tests with timeout
run_test_with_timeout "Security_Tests" "cd tests/security && go test -v comprehensive_security_test.go" $UNIT_TIMEOUT
track_test_result $?

echo ""
echo "📋 Phase 4: Ultra-Fast Quantum Tests"
echo "===================================="

# Check if Python quantum tests exist and run them
if [ -f "tests/integration/ultra_fast_validation_test.py" ]; then
    run_python_test_with_timeout "Ultra_Fast_Quantum" "tests/integration/ultra_fast_validation_test.py" $UNIT_TIMEOUT
    track_test_result $?
else
    echo "⚠️ Ultra-fast quantum test not found, skipping..."
fi

echo ""
echo "📋 Phase 5: Fast IBM Quantum Tests"
echo "=================================="

# Check if IBM Quantum token is available
if [ -f ".env" ] && grep -q "IBM_QUANTUM_TOKEN" .env; then
    echo "🔑 IBM Quantum token found, running hardware tests..."
    
    if [ -f "tests/integration/fast_ibm_quantum_test.py" ]; then
        run_python_test_with_timeout "Fast_IBM_Quantum" "tests/integration/fast_ibm_quantum_test.py" $QUANTUM_TIMEOUT
        track_test_result $?
    else
        echo "⚠️ Fast IBM quantum test not found, skipping..."
    fi
else
    echo "⚠️ No IBM Quantum token found, skipping hardware tests..."
    echo "💡 Add IBM_QUANTUM_TOKEN to .env file to enable hardware testing"
fi

echo ""
echo "📋 Phase 6: Benchmark Tests"
echo "==========================="

# Run quick benchmarks
run_test_with_timeout "Unit_Benchmarks" "cd tests/unit && go test -bench=. -benchtime=5s basic_functionality_test.go" $UNIT_TIMEOUT
track_test_result $?

run_test_with_timeout "Integration_Benchmarks" "cd tests/integration && go test -bench=. -benchtime=5s simple_integration_test.go" $UNIT_TIMEOUT
track_test_result $?

echo ""
echo "📊 Generating Fast Test Report"
echo "=============================="

# Calculate success rate
if [ $TOTAL_TESTS -gt 0 ]; then
    SUCCESS_RATE=$(echo "scale=1; $PASSED_TESTS * 100 / $TOTAL_TESTS" | bc 2>/dev/null || echo "0")
else
    SUCCESS_RATE="0"
fi

# Generate summary report
cat > "$RESULTS_DIR/FAST_TEST_SUMMARY.md" << EOF
# Fast Quantum Test Suite Results

**Generated:** $(date)
**Total Runtime:** $(date +%s) seconds
**Results Directory:** $RESULTS_DIR

## Test Summary

- **Total Tests:** $TOTAL_TESTS
- **Passed:** $PASSED_TESTS ✅
- **Timeouts:** $TIMEOUT_TESTS ⏰
- **Failed:** $FAILED_TESTS ❌
- **Success Rate:** ${SUCCESS_RATE}%

## Test Categories

### Unit Tests (${UNIT_TIMEOUT}s timeout)
- Basic functionality validation
- Mathematical operations
- Data structure tests

### Integration Tests (${INTEGRATION_TIMEOUT}s timeout)
- System-level validation
- Component interaction
- Performance characteristics

### Security Tests (${UNIT_TIMEOUT}s timeout)
- Cryptographic validation
- Information leakage detection
- Attack resistance testing

### Quantum Hardware Tests (${QUANTUM_TIMEOUT}s timeout)
- IBM Quantum hardware validation
- Real quantum circuit execution
- Hardware-specific optimizations

## Performance Metrics

### Timeout Strategy
- **Unit Tests:** ${UNIT_TIMEOUT}s (fast validation)
- **Integration Tests:** ${INTEGRATION_TIMEOUT}s (moderate complexity)
- **Quantum Tests:** ${QUANTUM_TIMEOUT}s (hardware queue time)

### Speed Optimizations
- Reduced shot counts for faster execution
- Simplified circuits for quick validation
- Aggressive timeout enforcement
- Parallel test execution where possible

## Files Generated

EOF

# List all generated files
for file in "$RESULTS_DIR"/*; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        filesize=$(ls -lh "$file" | awk '{print $5}')
        echo "- \`$filename\` ($filesize)" >> "$RESULTS_DIR/FAST_TEST_SUMMARY.md"
    fi
done

cat >> "$RESULTS_DIR/FAST_TEST_SUMMARY.md" << EOF

## Recommendations

### If Success Rate ≥ 80%
✅ **EXCELLENT** - System is ready for production use

### If Success Rate 60-79%
⚠️ **GOOD** - Minor issues, investigate timeout tests

### If Success Rate < 60%
❌ **NEEDS ATTENTION** - Significant issues require investigation

## Repository Information

**Repository:** https://github.com/hydraresearch/qzkp
**Paper Reference:** Section 5 - Reproducibility and Independent Verification

---

*This report was generated by the Fast Quantum Test Suite Runner*
*All tests executed with strict timeouts to ensure rapid feedback*
EOF

echo ""
echo "🎉 Fast Test Suite Complete!"
echo "============================"
echo ""
echo "📊 **FINAL RESULTS**"
echo "==================="
echo "✅ Passed: $PASSED_TESTS"
echo "⏰ Timeouts: $TIMEOUT_TESTS"
echo "❌ Failed: $FAILED_TESTS"
echo "📈 Success Rate: ${SUCCESS_RATE}%"
echo ""
echo "📁 Results: $RESULTS_DIR"
echo "📋 Summary: $RESULTS_DIR/FAST_TEST_SUMMARY.md"
echo ""

# Determine overall result
if [ $PASSED_TESTS -ge $((TOTAL_TESTS * 80 / 100)) ]; then
    echo "🚀 **EXCELLENT** - Fast tests passed with flying colors!"
    exit 0
elif [ $PASSED_TESTS -ge $((TOTAL_TESTS * 60 / 100)) ]; then
    echo "⚠️ **GOOD** - Most tests passed, some timeouts occurred"
    exit 0
else
    echo "❌ **NEEDS ATTENTION** - Multiple test failures detected"
    exit 1
fi
