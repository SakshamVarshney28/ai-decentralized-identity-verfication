# Virtual Environment Guide - What Runs Where

## 🐍 INSIDE Virtual Environment (venv)

**Everything Python-related runs INSIDE venv:**

### ✅ Install Python Packages
```cmd
# Activate venv first
venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # Linux/Mac

# Then install:
cd face_module
pip install -r requirements.txt

cd ../backend
pip install -r requirements.txt
```

### ✅ Run Django Server
```cmd
# Must be in venv
venv\Scripts\activate  # Windows
cd backend
python manage.py migrate
python manage.py runserver 8000
```

### ✅ Run Python Scripts
```cmd
# Must be in venv
venv\Scripts\activate
python manage.py shell
python manage.py test
```

---

## 🌐 OUTSIDE Virtual Environment

**Everything Node.js/JavaScript-related runs OUTSIDE venv:**

### ✅ Install Node.js Packages
```cmd
# DON'T activate venv for this
cd blockchain
npm install
```

### ✅ Run Ganache
```cmd
# DON'T activate venv
# In a NEW terminal (venv not activated)
npx ganache --port 7545 --deterministic
```

### ✅ Run Truffle Commands
```cmd
# DON'T activate venv
cd blockchain
npx truffle compile
npx truffle migrate --reset
```

### ✅ Run HTTP Server for Frontend
```cmd
# DON'T activate venv (optional, can use any method)
cd frontend
python -m http.server 3000
# OR just open index.html directly
```

---

## 📋 Complete Setup Flow

### Step 1: Create and Activate venv
```cmd
cd C:\Users\asus\verification-system
python -m venv venv
venv\Scripts\activate  # You should see (venv) in prompt
```

### Step 2: Install Python Packages (IN venv)
```cmd
# Make sure (venv) is in your prompt
cd face_module
pip install -r requirements.txt
cd ../backend
pip install -r requirements.txt
cd ..
```

### Step 3: Install Node Packages (OUTSIDE venv)
```cmd
# Open a NEW terminal (don't activate venv)
cd blockchain
npm install
cd ..
```

### Step 4: Start Ganache (OUTSIDE venv)
```cmd
# In the same terminal as Step 3, or new terminal
# DON'T activate venv
npx ganache --port 7545 --deterministic
# Keep this running!
```

### Step 5: Deploy Contract (OUTSIDE venv)
```cmd
# Open a NEW terminal (don't activate venv)
cd blockchain
npx truffle compile
npx truffle migrate --reset
cd ..
```

### Step 6: Run Django (IN venv)
```cmd
# Go back to your venv terminal (or activate venv)
venv\Scripts\activate  # Make sure (venv) is shown
cd backend
python manage.py migrate
python manage.py runserver 8000
# Keep this running!
```

### Step 7: Open Frontend (No venv needed)
```cmd
# Just open in browser or use HTTP server
# Option 1: Direct file open
# Navigate to frontend/index.html and double-click

# Option 2: HTTP server (no venv needed)
cd frontend
python -m http.server 3000
# Then open: http://localhost:3000/index.html
```

---

## 🎯 Quick Reference

| Task | venv Required? | Command |
|------|---------------|---------|
| Install Python packages | ✅ YES | `pip install -r requirements.txt` |
| Run Django server | ✅ YES | `python manage.py runserver` |
| Django migrations | ✅ YES | `python manage.py migrate` |
| Install Node packages | ❌ NO | `npm install` |
| Run Ganache | ❌ NO | `npx ganache --port 7545` |
| Truffle commands | ❌ NO | `npx truffle migrate` |
| Open frontend | ❌ NO | Just open in browser |

---

## 💡 Pro Tips

1. **Keep 3 terminals open:**
   - Terminal 1: venv activated → Django server
   - Terminal 2: No venv → Ganache
   - Terminal 3: No venv → Truffle (when needed)

2. **How to know if venv is active:**
   - Windows: `(venv) C:\Users\...>`
   - Linux/Mac: `(venv) user@computer:~$`

3. **If you forget to activate venv:**
   - Django will fail with "No module named django"
   - Just activate it: `venv\Scripts\activate`

4. **If you activate venv for Node.js:**
   - It won't hurt, but it's unnecessary
   - Node.js doesn't use Python venv

---

## ✅ Summary

**IN venv:**
- ✅ All Python commands
- ✅ pip install
- ✅ Django server
- ✅ Python scripts

**OUTSIDE venv:**
- ✅ npm install
- ✅ npx commands (ganache, truffle)
- ✅ Opening browser
- ✅ File operations

---

**Remember:** Python = venv, Node.js = no venv! 🎯

