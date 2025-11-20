@echo off
REM FaceAuth MVP Demo Script for Windows
REM This script sets up and runs the complete FaceAuth system on Windows

echo 🚀 Starting FaceAuth MVP Demo Setup
echo ==================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.7+
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found. Please install Node.js 14+
    pause
    exit /b 1
)

echo [INFO] Prerequisites check passed

REM Install dependencies
echo [STEP] Installing dependencies...

echo [INFO] Installing face recognition dependencies...
cd face_module
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install face recognition dependencies
    pause
    exit /b 1
)
cd ..

echo [INFO] Installing Django backend dependencies...
cd backend
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install Django dependencies
    pause
    exit /b 1
)
cd ..

echo [INFO] Installing blockchain dependencies...
cd blockchain
npm install
if errorlevel 1 (
    echo [ERROR] Failed to install blockchain dependencies
    pause
    exit /b 1
)
cd ..

REM Start Ganache
echo [STEP] Starting Ganache blockchain...
cd blockchain
start "Ganache" cmd /k "npx ganache-cli --port 7545 --deterministic"
timeout /t 5 /nobreak >nul
cd ..

echo [INFO] Ganache started on port 7545

REM Deploy smart contract
echo [STEP] Deploying smart contract...
cd blockchain
npx truffle compile
if errorlevel 1 (
    echo [ERROR] Failed to compile smart contract
    pause
    exit /b 1
)

npx truffle migrate --reset
if errorlevel 1 (
    echo [ERROR] Failed to deploy smart contract
    pause
    exit /b 1
)
cd ..

echo [INFO] Smart contract deployed successfully

REM Start Django backend
echo [STEP] Starting Django backend...
cd backend
python manage.py migrate
if errorlevel 1 (
    echo [ERROR] Failed to run Django migrations
    pause
    exit /b 1
)

start "Django Server" cmd /k "python manage.py runserver 8000"
timeout /t 3 /nobreak >nul
cd ..

echo [INFO] Django backend started on port 8000

REM Open frontend
echo [STEP] Opening frontend...
start frontend\index.html

echo [INFO] Frontend opened in browser

REM Display instructions
echo.
echo 🎉 FaceAuth MVP is now running!
echo.
echo 📋 What you can do:
echo 1. Open http://localhost:8000 or the frontend\index.html file
echo 2. Register a new user with username, password, and face capture
echo 3. Login with the same credentials and face
echo 4. View the dashboard with your authentication data
echo.
echo 🔧 Services running:
echo - Ganache: http://localhost:7545
echo - Django API: http://localhost:8000
echo - Frontend: frontend\index.html
echo.
echo ⚠️  Important Notes:
echo - Make sure your camera is working for face capture
echo - The system processes faces locally (no images stored on blockchain)
echo - All data is hashed before blockchain storage
echo.
echo 🛑 To stop the demo:
echo - Close the Ganache and Django command windows
echo - Or press Ctrl+C in each window
echo.

pause

