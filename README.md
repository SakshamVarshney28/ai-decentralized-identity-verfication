# 🟣 FaceAuth – Decentralized Facial Authentication System

FaceAuth is a complete **password + face recognition authentication system** powered by:

- **Django** (backend API)
- **Face Recognition + dlib** (face encoding)
- **Ethereum Blockchain (Ganache + Truffle)** for decentralized credential storage
- **Vanilla JavaScript + Camera API** (frontend)

This project captures a user’s face encoding, hashes it, and stores it *along with password hash* inside a **smart contract on a local blockchain**.

---

# 🚀 Features

### 🔐 Authentication
- Register with username + password + facial data  
- Login using password + live face scan  
- Blockchain verifies both hashes

### 🧠 Face Recognition
- dlib-based feature encoding  
- Generates 128-dimension facial embeddings  
- Encodings hashed before blockchain storage

### ⛓ Blockchain Storage
- Smart contract stores:
  - Username  
  - Password hash  
  - Face hash  
- No database needed — fully decentralized

### 📸 Frontend UI
- Webcam capture  
- Instant preview  
- Dashboard for stored credentials  

---

# 🧰 Prerequisites

| Tool | Required Version |
|------|-----------------|
| Python | **3.10.x** |
| Node.js | **18.x** |
| npm | Latest |
| Ganache CLI |
| Visual Studio Build Tools | Required for dlib |
| Webcam | Required |

---

# ⚙️ Installation Guide

## 1️⃣ Create Virtual Environment

```cmd
cd verification-system
python -m venv venv
venv\Scripts\activate
```

---

## 2️⃣ Install dlib + face_recognition

### Download dlib wheel (Windows, Python 3.10)

```
https://github.com/sachadee/Dlib/blob/main/dlib-19.22.99-cp310-cp310-win_amd64.whl
```

### Install:

```cmd
cd face_module
pip install dlib-19.22.99-cp310-cp310-win_amd64.whl
pip install git+https://github.com/ageitgey/face_recognition.git
pip install numpy Pillow opencv-python cmake
cd ..
```

---

## 3️⃣ Install Django dependencies

```cmd
cd backend
pip install -r requirements.txt
cd ..
```

---

## 4️⃣ Install Blockchain dependencies (Node.js)

```cmd
cd blockchain
npm install
cd ..
```

---

## 5️⃣ Start Ganache Blockchain

```cmd
npx ganache --port 7545 --deterministic
```

Keep Ganache running.

---

## 6️⃣ Deploy Smart Contract

```cmd
cd blockchain
npx truffle compile
npx truffle migrate --reset
```

Copy the generated contract address.

---

## 7️⃣ Add Contract Address to Django

Open:

```
backend/authentication/views.py
```

Replace:

```python
CONTRACT_ADDRESS = None
```

With:

```python
CONTRACT_ADDRESS = "0xYOUR_DEPLOYED_ADDRESS"
```

---

## 8️⃣ Run Django Server

```cmd
cd backend
python manage.py migrate
python manage.py runserver 8000
```

Backend URL:

👉 http://127.0.0.1:8000/

---

## 9️⃣ Run Frontend

```cmd
cd frontend
python -m http.server 3000
```

Frontend URL:

👉 http://localhost:3000/index.html

---

# 🧪 Usage

## 🔵 Registration

1. Go to **Register** tab  
2. Enter username & password  
3. Allow camera permissions  
4. Capture face  
5. Click **Register**  
6. Data is encoded → hashed → stored on blockchain  

## 🟣 Login

1. Enter username + password  
2. Capture face  
3. Click **Login**  
4. Hashes are verified with blockchain  

## 🟢 Dashboard

Displays:

- Username  
- Password hash  
- Face encoding  
- Face hash  
- Smart contract response  

---

