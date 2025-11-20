# FaceAuth MVP - Demo Instructions

## 🎯 Quick Start

### Option 1: Automated Setup (Recommended)

**For Linux/Mac:**
```bash
# Make scripts executable
chmod +x run_demo.sh install_dependencies.sh

# Install dependencies
./install_dependencies.sh

# Run the demo
./run_demo.sh
```

**For Windows:**
```cmd
REM Install dependencies
setup_windows.bat

REM Run the demo
run_demo.bat
```

### Option 2: Manual Setup

1. **Install Dependencies**
   ```bash
   # Face recognition
   cd face_module
   pip install -r requirements.txt
   
   # Django backend
   cd ../backend
   pip install -r requirements.txt
   
   # Blockchain
   cd ../blockchain
   npm install
   ```

2. **Start Ganache**
   ```bash
   npx ganache-cli --port 7545 --deterministic
   ```

3. **Deploy Smart Contract**
   ```bash
   cd blockchain
   npx truffle compile
   npx truffle migrate --reset
   ```

4. **Start Django Backend**
   ```bash
   cd ../backend
   python manage.py migrate
   python manage.py runserver 8000
   ```

5. **Open Frontend**
   - Open `frontend/index.html` in your browser
   - Or serve it via a local server

## 🎮 Demo Workflow

### 1. Registration
1. Open the frontend in your browser
2. Click "Register" tab
3. Enter username and password
4. Click "Start Camera" (allow camera access)
5. Click "Capture Face" when ready
6. Click "Register User"

### 2. Login
1. Click "Login" tab
2. Enter your username and password
3. Click "Start Camera" (allow camera access)
4. Click "Capture Face" when ready
5. Click "Login"

### 3. Dashboard
After successful login, you'll see:
- Username
- Password hash (SHA-256)
- Face encoding (128-dimensional vector)
- Face hash (SHA-256)

## 🔧 Troubleshooting

### Camera Issues
- **Problem**: Camera not working
- **Solution**: 
  - Use HTTPS or localhost
  - Check browser permissions
  - Try Chrome/Firefox

### Face Detection Issues
- **Problem**: Face not detected
- **Solution**:
  - Ensure good lighting
  - Face should be clearly visible
  - Try different angles

### Blockchain Issues
- **Problem**: Contract deployment failed
- **Solution**:
  - Check if Ganache is running
  - Verify port 7545 is available
  - Check Truffle configuration

### Django Issues
- **Problem**: Server not starting
- **Solution**:
  - Check if port 8000 is available
  - Verify Python dependencies
  - Check Django logs

## 📊 Expected Results

### Successful Registration
```json
{
  "success": true,
  "message": "User registered successfully",
  "username": "testuser",
  "password_hash": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
  "face_hash": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"
}
```

### Successful Login
```json
{
  "success": true,
  "message": "Login successful",
  "dashboard_data": {
    "username": "testuser",
    "password_hash": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
    "face_encoding": [0.1, 0.2, 0.3, ...], // 128-dimensional array
    "face_hash": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"
  }
}
```

## 🛑 Stopping the Demo

### Automated Scripts
- Press `Ctrl+C` in the terminal running the script
- Close any opened command windows

### Manual Setup
- Stop Ganache: Close the Ganache terminal
- Stop Django: Press `Ctrl+C` in the Django terminal
- Close browser tabs

## 📝 Notes

- **Privacy**: All face processing happens locally
- **Security**: Only hashes are stored on blockchain
- **Performance**: Face recognition takes 2-3 seconds
- **Compatibility**: Works best with Chrome/Firefox

## 🎯 Demo Checklist

- [ ] Ganache running on port 7545
- [ ] Smart contract deployed
- [ ] Django server running on port 8000
- [ ] Frontend accessible in browser
- [ ] Camera permissions granted
- [ ] Face detection working
- [ ] Registration successful
- [ ] Login successful
- [ ] Dashboard displaying data

## 🆘 Getting Help

If you encounter issues:
1. Check the troubleshooting section above
2. Review the console logs
3. Verify all services are running
4. Check the README.md for detailed documentation
5. Contact the development team

---

**Happy Demo! 🎉**

