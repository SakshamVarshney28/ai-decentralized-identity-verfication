#!/bin/bash

# FaceAuth MVP Demo Script
# This script sets up and runs the complete FaceAuth system

set -e  # Exit on any error

echo "🚀 Starting FaceAuth MVP Demo Setup"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    print_error "Python not found. Please install Python 3.7+"
    exit 1
fi

print_status "Python found: $($PYTHON_CMD --version)"

# Check Node.js
if command -v node &> /dev/null; then
    print_status "Node.js found: $(node --version)"
else
    print_error "Node.js not found. Please install Node.js 14+"
    exit 1
fi

# Check if Ganache is available
if command -v ganache-cli &> /dev/null; then
    GANACHE_CMD="ganache-cli"
elif command -v ganache &> /dev/null; then
    GANACHE_CMD="ganache"
else
    print_warning "Ganache not found. Will install via npm."
fi

# Step 2: Install dependencies
print_step "2. Installing dependencies..."

# Install face module dependencies
print_status "Installing face recognition dependencies..."
cd face_module
if [ "$IS_WINDOWS" = true ]; then
    $PYTHON_CMD -m pip install -r requirements.txt
else
    $PYTHON_CMD -m pip install -r requirements.txt
fi
cd ..

# Install backend dependencies
print_status "Installing Django backend dependencies..."
cd backend
$PYTHON_CMD -m pip install -r requirements.txt
cd ..

# Install blockchain dependencies
print_status "Installing blockchain dependencies..."
cd blockchain
if [ "$IS_WINDOWS" = true ]; then
    npm install
else
    npm install
fi
cd ..

# Step 3: Start Ganache
print_step "3. Starting Ganache blockchain..."

# Kill any existing Ganache processes
if [ "$IS_WINDOWS" = true ]; then
    taskkill //F //IM node.exe 2>/dev/null || true
else
    pkill -f ganache 2>/dev/null || true
fi

# Start Ganache in background
cd blockchain
if [ "$IS_WINDOWS" = true ]; then
    start "Ganache" cmd /k "npx ganache-cli --port 7545 --deterministic"
    sleep 5
else
    npx ganache-cli --port 7545 --deterministic &
    GANACHE_PID=$!
    sleep 5
fi
cd ..

print_status "Ganache started on port 7545"

# Step 4: Deploy smart contract
print_step "4. Deploying smart contract..."

cd blockchain
npx truffle compile
npx truffle migrate --reset
cd ..

print_status "Smart contract deployed successfully"

# Step 5: Start Django backend
print_step "5. Starting Django backend..."

cd backend
$PYTHON_CMD manage.py migrate
$PYTHON_CMD manage.py runserver 8000 &
DJANGO_PID=$!
cd ..

print_status "Django backend started on port 8000"

# Step 6: Open frontend
print_step "6. Opening frontend..."

if [ "$IS_WINDOWS" = true ]; then
    start frontend/index.html
else
    if command -v xdg-open &> /dev/null; then
        xdg-open frontend/index.html
    elif command -v open &> /dev/null; then
        open frontend/index.html
    else
        print_warning "Could not automatically open browser. Please open frontend/index.html manually"
    fi
fi

print_status "Frontend opened in browser"

# Step 7: Display instructions
print_step "7. Demo Instructions"
echo ""
echo "🎉 FaceAuth MVP is now running!"
echo ""
echo "📋 What you can do:"
echo "1. Open http://localhost:8000 or the frontend/index.html file"
echo "2. Register a new user with username, password, and face capture"
echo "3. Login with the same credentials and face"
echo "4. View the dashboard with your authentication data"
echo ""
echo "🔧 Services running:"
echo "- Ganache: http://localhost:7545"
echo "- Django API: http://localhost:8000"
echo "- Frontend: frontend/index.html"
echo ""
echo "⚠️  Important Notes:"
echo "- Make sure your camera is working for face capture"
echo "- The system processes faces locally (no images stored on blockchain)"
echo "- All data is hashed before blockchain storage"
echo ""
echo "🛑 To stop the demo:"
echo "- Press Ctrl+C to stop this script"
echo "- Or manually stop Ganache and Django processes"
echo ""

# Wait for user input to stop
echo "Press Ctrl+C to stop the demo..."
trap 'print_status "Stopping demo..."; kill $DJANGO_PID 2>/dev/null || true; kill $GANACHE_PID 2>/dev/null || true; exit 0' INT

# Keep the script running
while true; do
    sleep 1
done

