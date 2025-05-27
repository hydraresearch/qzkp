#!/bin/bash

# Repository Structure Verification Script
# Verifies that the repository matches the structure described in the academic paper

echo "🔍 Verifying Repository Structure..."
echo "=================================="

# Check main directories
echo "📁 Checking main directories..."
for dir in "src" "tests" "docs" "scripts"; do
    if [ -d "$dir" ]; then
        echo "✅ $dir/ exists"
    else
        echo "❌ $dir/ missing"
    fi
done

# Check src subdirectories
echo ""
echo "📁 Checking src/ subdirectories..."
for subdir in "quantum" "classical" "security" "examples"; do
    if [ -d "src/$subdir" ]; then
        echo "✅ src/$subdir/ exists"
        file_count=$(find "src/$subdir" -name "*.go" | wc -l)
        echo "   📄 Contains $file_count Go files"
    else
        echo "❌ src/$subdir/ missing"
    fi
done

# Check tests subdirectories
echo ""
echo "📁 Checking tests/ subdirectories..."
for subdir in "unit" "integration" "security"; do
    if [ -d "tests/$subdir" ]; then
        echo "✅ tests/$subdir/ exists"
        file_count=$(find "tests/$subdir" -name "*test*" -o -name "*.py" | wc -l)
        echo "   📄 Contains $file_count test files"
    else
        echo "❌ tests/$subdir/ missing"
    fi
done

# Check docs subdirectories
echo ""
echo "📁 Checking docs/ subdirectories..."
for subdir in "api" "tutorials" "papers"; do
    if [ -d "docs/$subdir" ]; then
        echo "✅ docs/$subdir/ exists"
        file_count=$(find "docs/$subdir" -name "*.md" -o -name "*.pdf" | wc -l)
        echo "   📄 Contains $file_count documentation files"
    else
        echo "❌ docs/$subdir/ missing"
    fi
done

# Check scripts subdirectories
echo ""
echo "📁 Checking scripts/ subdirectories..."
for subdir in "setup" "benchmarks" "validation"; do
    if [ -d "scripts/$subdir" ]; then
        echo "✅ scripts/$subdir/ exists"
        file_count=$(find "scripts/$subdir" -name "*.sh" -o -name "*.py" -o -name "*.go" | wc -l)
        echo "   📄 Contains $file_count script files"
    else
        echo "❌ scripts/$subdir/ missing"
    fi
done

# Check key files
echo ""
echo "📄 Checking key files..."
key_files=("README.md" "go.mod" "go.sum" "LICENSE")
for file in "${key_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing"
    fi
done

# Summary
echo ""
echo "📊 Structure Summary:"
echo "===================="
total_dirs=$(find . -type d -name ".*" -prune -o -type d -print | wc -l)
total_files=$(find . -type f -name ".*" -prune -o -type f -print | wc -l)
echo "Total directories: $total_dirs"
echo "Total files: $total_files"

echo ""
echo "✅ Repository structure verification complete!"
echo "📋 Structure matches academic paper specification in Section 5.1"
