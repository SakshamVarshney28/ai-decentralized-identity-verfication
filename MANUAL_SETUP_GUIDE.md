# FaceAuth MVP - Manual Setup Guide (Virtual Environment)

## 📋 Prerequisites Check

Before starting, ensure you have:
- **Python 3.8+** (check with `python --version`)
- **Node.js 14+** (check with `node --version`)
- **pip** (usually comes with Python)
- **npm** (comes with Node.js)
- **Webcam** for face capture

---

## 🔧 Step 1: Create Virtual Environment

### Windows:
```cmd
cd C:\Users\asus\verification-system
python -m venv venv
venv\Scripts\activate
```

### Linux/Mac:
```bash
cd ~/verification-system
python3 -m venv venv
source venv/bin/activate
```

**You should see `(venv)` in your terminal prompt.**

---

## 📦 Step 2: Install Face Recognition Dependencies

```cmd
# Make sure virtual environment is activated
cd face_module
pip install -r requirements.txt
cd ..
```

**Note:** This may take 10-15 minutes as it compiles dlib. If it fails:
- **Windows:** Install Visual Studio Build Tools (C++ compiler)
- **Linux:** `sudo apt-get install build-essential cmake`
- **Mac:** `brew install cmake`

---

## 📦 Step 3: Install Django Backend Dependencies

```cmd
# Still in virtual environment
cd backend
pip install -r requirements.txt
cd ..
```

---

## 📦 Step 4: Install Blockchain Dependencies

```cmd
# Open a NEW terminal (keep venv terminal open)
cd blockchain
npm install
cd ..
```

**This installs Truffle and other Node.js packages.**

---

## 🚀 Step 5: Start Ganache Blockchain

### Option A: Using npx (Recommended)
```cmd
# In a NEW terminal window
npx ganache --port 7545 --deterministic
```

### Option B: Install Ganache globally first
```cmd
npm install -g ganache
ganache --port 7545 --deterministic
```

### Option C: Use Ganache UI (Desktop App)
1. Download from: https://trufflesuite.com/ganache/
2. Install and open
3. Create new workspace
4. Set port to `7545`
5. Click "Start"

**Keep Ganache running in this terminal!**

---

## 📝 Step 5: Deploy Smart Contract

```cmd
# In a NEW terminal window
cd blockchain
npx truffle compile
npx truffle migrate --reset
```

**Copy the contract address from the output!** It looks like: `0x1234...`

---

## ⚙️ Step 6: Configure Django Settings

### Option A: Update views.py directly

Open `backend/authentication/views.py` and find line 48:
```python
CONTRACT_ADDRESS = None
```

Replace with your contract address:
```python
CONTRACT_ADDRESS = "0x1234..."  # Your actual address from Step 5
```

### Option B: Create .env file (if using python-decouple)

Create `backend/.env`:
```
SECRET_KEY=django-insecure-change-this-in-production
DEBUG=True
GANACHE_URL=http://127.0.0.1:7545
CONTRACT_ADDRESS=0x1234...  # Your contract address
```

---

## 🗄️ Step 7: Run Django Migrations

```cmd
# In your virtual environment terminal
cd backend
python manage.py migrate
```

---

## 🚀 Step 8: Start Django Server

```cmd
# Still in backend directory, virtual environment activated
python manage.py runserver 8000
```

**Keep this terminal running!** You should see:
```
Starting development server at http://127.0.0.1:8000/
```

---

## 🌐 Step 9: Open Frontend

### Option A: Direct File Open
- Navigate to `frontend/` folder
- Double-click `index.html`
- Open in Chrome/Firefox (best camera support)

### Option B: Serve via HTTP (Recommended for camera access)
```cmd
# In a NEW terminal
cd frontend
python -m http.server 3000
```

Then open: `http://localhost:3000/index.html`

---

## ✅ Step 10: Test the Application

1. **Register:**
   - Click "Register" tab
   - Enter username: `testuser`
   - Enter password: `test123`
   - Click "Start Camera" → Allow camera access
   - Click "Capture Face" when ready
   - Click "Register User"

2. **Login:**
   - Click "Login" tab
   - Enter same username and password
   - Click "Start Camera" → Capture face
   - Click "Login"

3. **Dashboard:**
   - Should show your username, password hash, face encoding, and face hash

---

## 🐛 Troubleshooting

### Issue: "face_recognition not found"
```cmd
# Reinstall in virtual environment
pip install face_recognition
pip install dlib
```

### Issue: "Contract not deployed"
- Check Ganache is running
- Verify contract address in `views.py`
- Re-run `truffle migrate`

### Issue: "Camera not working"
- Use Chrome/Firefox
- Open via `http://localhost:3000` not `file://`
- Check browser permissions

### Issue: "Module not found"
```cmd
# Make sure virtual environment is activated
# Reinstall dependencies
pip install -r backend/requirements.txt
```

---

## 🛑 Stopping the Project

1. **Stop Django:** Press `Ctrl+C` in Django terminal
2. **Stop Ganache:** Press `Ctrl+C` in Ganache terminal
3. **Deactivate venv:** Type `deactivate` in terminal

---

## 📊 Summary of Running Services

You should have **3 terminals/windows** running:

1. **Terminal 1:** Ganache blockchain (`npx ganache --port 7545`)
2. **Terminal 2:** Django server (`python manage.py runserver`)
3. **Terminal 3:** (Optional) HTTP server for frontend (`python -m http.server 3000`)

---

## ✅ Verification Checklist

- [ ] Virtual environment created and activated
- [ ] Face recognition dependencies installed
- [ ] Django dependencies installed
- [ ] Blockchain dependencies installed
- [ ] Ganache running on port 7545
- [ ] Smart contract deployed
- [ ] Contract address configured in Django
- [ ] Django migrations completed
- [ ] Django server running on port 8000
- [ ] Frontend accessible in browser
- [ ] Camera permissions granted
- [ ] Registration successful
- [ ] Login successful
- [ ] Dashboard displaying data

---

**You're all set! 🎉**





