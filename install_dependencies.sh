#!/bin/bash

# FaceAuth MVP - Dependency Installation Script
# This script installs all required dependencies for the FaceAuth system

set -e  # Exit on any error

echo "🔧 Installing FaceAuth MVP Dependencies"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Check if running on Windows
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "win32" ]]; then
    IS_WINDOWS=true
    print_warning "Windows detected. Some commands may need adjustment."
else
    IS_WINDOWS=false
fi

# Step 1: Check prerequisites
print_step "1. Checking prerequisites..."

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    PIP_CMD="pip"
else
    print_error "Python not found. Please install Python 3.7+"
    exit 1
fi

print_status "Python found: $($PYTHON_CMD --version)"

# Check pip
if ! command -v $PIP_CMD &> /dev/null; then
    print_error "pip not found. Please install pip"
    exit 1
fi

print_status "pip found: $($PIP_CMD --version)"

# Check Node.js
if command -v node &> /dev/null; then
    print_status "Node.js found: $(node --version)"
else
    print_error "Node.js not found. Please install Node.js 14+"
    exit 1
fi

# Check npm
if command -v npm &> /dev/null; then
    print_status "npm found: $(npm --version)"
else
    print_error "npm not found. Please install npm"
    exit 1
fi

# Step 2: Install system dependencies (if needed)
print_step "2. Installing system dependencies..."

# For face recognition, we need some system libraries
if [ "$IS_WINDOWS" = false ]; then
    print_status "Installing system dependencies for face recognition..."
    
    # Check if we're on Ubuntu/Debian
    if command -v apt-get &> /dev/null; then
        print_status "Detected Ubuntu/Debian. Installing system packages..."
        sudo apt-get update
        sudo apt-get install -y python3-dev python3-pip build-essential cmake
        sudo apt-get install -y libopenblas-dev liblapack-dev libx11-dev libgtk-3-dev
        sudo apt-get install -y libboost-python-dev libboost-system-dev
    # Check if we're on macOS
    elif command -v brew &> /dev/null; then
        print_status "Detected macOS. Installing system packages..."
        brew install cmake
        brew install boost-python
    else
        print_warning "System dependencies may need to be installed manually"
        print_warning "Required: cmake, boost-python, openblas, lapack"
    fi
else
    print_warning "Windows detected. System dependencies should be handled by pip"
fi

# Step 3: Install Python dependencies
print_step "3. Installing Python dependencies..."

# Install face recognition dependencies
print_status "Installing face recognition dependencies..."
cd face_module
$PIP_CMD install -r requirements.txt
cd ..

# Install backend dependencies
print_status "Installing Django backend dependencies..."
cd backend
$PIP_CMD install -r requirements.txt
cd ..

# Step 4: Install Node.js dependencies
print_step "4. Installing Node.js dependencies..."

print_status "Installing blockchain dependencies..."
cd blockchain
npm install
cd ..

# Step 5: Verify installations
print_step "5. Verifying installations..."

# Test Python imports
print_status "Testing Python imports..."
$PYTHON_CMD -c "import face_recognition; print('face_recognition: OK')" || print_warning "face_recognition import failed"
$PYTHON_CMD -c "import dlib; print('dlib: OK')" || print_warning "dlib import failed"
$PYTHON_CMD -c "import django; print('Django: OK')" || print_warning "Django import failed"
$PYTHON_CMD -c "import web3; print('Web3: OK')" || print_warning "Web3 import failed"

# Test Node.js packages
print_status "Testing Node.js packages..."
cd blockchain
npx truffle version || print_warning "Truffle not found"
cd ..

print_status "Dependency installation completed!"

# Step 6: Display next steps
print_step "6. Next Steps"
echo ""
echo "🎉 All dependencies have been installed!"
echo ""
echo "📋 To run the FaceAuth MVP:"
echo "1. Run: ./run_demo.sh"
echo "2. Or follow the manual setup in README.md"
echo ""
echo "🔧 Manual setup:"
echo "1. Start Ganache: npx ganache-cli --port 7545"
echo "2. Deploy contract: cd blockchain && npx truffle migrate"
echo "3. Start Django: cd backend && python manage.py runserver"
echo "4. Open frontend/index.html in browser"
echo ""
echo "⚠️  Note: Face recognition requires camera access"
echo "⚠️  Note: Some dependencies may take time to compile"
echo ""

