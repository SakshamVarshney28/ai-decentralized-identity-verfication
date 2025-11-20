@echo off
REM FaceAuth MVP - Windows Setup Script
REM This script installs all required dependencies for the FaceAuth system on Windows

echo 🔧 Installing FaceAuth MVP Dependencies
echo ======================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)
echo [INFO] Python found

REM Check if pip is installed
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip not found. Please install pip
    pause
    exit /b 1
)
echo [INFO] pip found

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found. Please install Node.js 14+ from https://nodejs.org
    pause
    exit /b 1
)
echo [INFO] Node.js found

REM Check if npm is installed
npm --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] npm not found. Please install npm
    pause
    exit /b 1
)
echo [INFO] npm found

echo [STEP] Installing Python dependencies...

echo [INFO] Installing face recognition dependencies...
cd face_module
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install face recognition dependencies
    echo [WARNING] You may need to install Visual Studio Build Tools
    echo [WARNING] Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
    pause
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

echo [STEP] Installing Node.js dependencies...

echo [INFO] Installing blockchain dependencies...
cd blockchain
npm install
if errorlevel 1 (
    echo [ERROR] Failed to install blockchain dependencies
    pause
    exit /b 1
)
cd ..

echo [STEP] Verifying installations...

echo [INFO] Testing Python imports...
python -c "import face_recognition; print('face_recognition: OK')" 2>nul || echo [WARNING] face_recognition import failed
python -c "import dlib; print('dlib: OK')" 2>nul || echo [WARNING] dlib import failed
python -c "import django; print('Django: OK')" 2>nul || echo [WARNING] Django import failed
python -c "import web3; print('Web3: OK')" 2>nul || echo [WARNING] Web3 import failed

echo [INFO] Testing Node.js packages...
cd blockchain
npx truffle version 2>nul || echo [WARNING] Truffle not found
cd ..

echo [INFO] Dependency installation completed!

echo.
echo 🎉 All dependencies have been installed!
echo.
echo 📋 To run the FaceAuth MVP:
echo 1. Run: run_demo.bat
echo 2. Or follow the manual setup in README.md
echo.
echo 🔧 Manual setup:
echo 1. Start Ganache: npx ganache-cli --port 7545
echo 2. Deploy contract: cd blockchain ^&^& npx truffle migrate
echo 3. Start Django: cd backend ^&^& python manage.py runserver
echo 4. Open frontend\index.html in browser
echo.
echo ⚠️  Note: Face recognition requires camera access
echo ⚠️  Note: Some dependencies may take time to compile
echo.

pause
