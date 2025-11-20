# FaceAuth MVP - AI Face Recognition + Blockchain Authentication

A Minimum Viable Product (MVP) for an AI-based face recognition system with blockchain authentication using Ethereum smart contracts.

## 🎯 Features

- **Face Recognition**: Local face processing using Python `face_recognition` and `dlib`
- **Blockchain Storage**: User credentials stored on Ethereum smart contract via Ganache
- **Secure Hashing**: SHA-256 hashing for passwords and face encodings
- **Web Interface**: Modern HTML/JS frontend with camera capture
- **Django Backend**: RESTful API with Web3.py integration
- **Privacy First**: No raw images stored on-chain, all processing happens locally

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Django API    │    │   Smart Contract│
│   (HTML/JS)     │◄──►│   (Python)      │◄──►│   (Solidity)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Camera        │    │   Face Utils    │    │   Ganache       │
│   Capture       │    │   (dlib/face)   │    │   (Local Chain) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
verification-system/
├── backend/                 # Django backend
│   ├── faceauth_backend/    # Django project settings
│   ├── authentication/      # Django app for auth endpoints
│   ├── requirements.txt     # Python dependencies
│   └── manage.py           # Django management script
├── face_module/            # Face recognition utilities
│   ├── face_utils.py       # Core face processing functions
│   ├── test_face_utils.py  # Unit tests
│   └── requirements.txt    # Face recognition dependencies
├── blockchain/             # Smart contract and deployment
│   ├── contracts/          # Solidity contracts
│   ├── migrations/         # Truffle migrations
│   ├── test/              # Contract tests
│   └── truffle-config.js  # Truffle configuration
├── frontend/              # Web interface
│   ├── index.html         # Main login/register page
│   ├── dashboard.html     # User dashboard
│   └── script.js         # Frontend JavaScript
├── run_demo.sh           # Demo setup script
└── README.md            # This file
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.7+** with pip
- **Node.js 14+** with npm
- **Webcam** for face capture
- **Git** (optional, for cloning)

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd verification-system
   ```

2. **Run the demo script**
   ```bash
   # On Linux/Mac
   chmod +x run_demo.sh
   ./run_demo.sh
   
   # On Windows
   bash run_demo.sh
   ```

   The script will:
   - Install all dependencies
   - Start Ganache blockchain
   - Deploy smart contract
   - Start Django backend
   - Open the frontend

### Manual Setup (Alternative)

If the demo script doesn't work, follow these manual steps:

#### 1. Install Dependencies

```bash
# Face recognition dependencies
cd face_module
pip install -r requirements.txt
cd ..

# Django backend dependencies
cd backend
pip install -r requirements.txt
cd ..

# Blockchain dependencies
cd blockchain
npm install
cd ..
```

#### 2. Start Ganache

```bash
cd blockchain
npx ganache-cli --port 7545 --deterministic
```

#### 3. Deploy Smart Contract

```bash
# In a new terminal
cd blockchain
npx truffle compile
npx truffle migrate --reset
```

#### 4. Start Django Backend

```bash
# In a new terminal
cd backend
python manage.py migrate
python manage.py runserver 8000
```

#### 5. Open Frontend

Open `frontend/index.html` in your browser.

## 🎮 Usage

### Registration

1. Open the frontend in your browser
2. Click "Register" tab
3. Enter username and password
4. Click "Start Camera" and allow camera access
5. Click "Capture Face" when ready
6. Click "Register User"

### Login

1. Click "Login" tab
2. Enter your username and password
3. Click "Start Camera" and allow camera access
4. Click "Capture Face" when ready
5. Click "Login"

### Dashboard

After successful login, you'll see:
- Username
- Password hash (SHA-256)
- Face encoding (128-dimensional vector)
- Face hash (SHA-256)

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `backend/` directory:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
GANACHE_URL=http://127.0.0.1:7545
CONTRACT_ADDRESS=0x...  # Set after deployment
PRIVATE_KEY=0x...       # Ganache private key
```

### Smart Contract Address

After deployment, update the contract address in:
- `backend/authentication/views.py`
- Frontend API calls (if needed)

## 🧪 Testing

### Run Unit Tests

```bash
# Face module tests
cd face_module
python test_face_utils.py

# Smart contract tests
cd blockchain
npx truffle test
```

### Test Coverage

- ✅ Face encoding and hashing
- ✅ Face verification
- ✅ Smart contract functions
- ✅ User registration/login
- ✅ API endpoints

## 🔒 Security Features

- **Local Processing**: All face recognition happens locally
- **Hashed Storage**: Only hashes stored on blockchain
- **No Raw Images**: Images never leave the user's device
- **SHA-256 Hashing**: Secure password and face encoding hashing
- **Private Keys**: Secure key management for blockchain transactions

## 🐛 Troubleshooting

### Common Issues

1. **Camera not working**
   - Check browser permissions
   - Try HTTPS (required for camera access)
   - Use Chrome/Firefox (best compatibility)

2. **Face not detected**
   - Ensure good lighting
   - Face should be clearly visible
   - Try different angles

3. **Blockchain connection failed**
   - Check if Ganache is running
   - Verify port 7545 is available
   - Check contract deployment

4. **Django server issues**
   - Check if port 8000 is available
   - Verify Python dependencies
   - Check Django logs

### Debug Mode

Enable debug logging:

```python
# In backend/faceauth_backend/settings.py
DEBUG = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
```

## 📚 API Documentation

### Endpoints

#### POST /api/register/
Register a new user.

**Request:**
```json
{
    "username": "string",
    "password": "string",
    "face_image": "base64_encoded_image"
}
```

**Response:**
```json
{
    "success": true,
    "message": "User registered successfully",
    "username": "string",
    "password_hash": "string",
    "face_hash": "string"
}
```

#### POST /api/verify/
Verify user login.

**Request:**
```json
{
    "username": "string",
    "password": "string",
    "face_image": "base64_encoded_image"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Login successful",
    "dashboard_data": {
        "username": "string",
        "password_hash": "string",
        "face_encoding": [128_dimensional_array],
        "face_hash": "string"
    }
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [face_recognition](https://github.com/ageitgey/face_recognition) - Face recognition library
- [dlib](http://dlib.net/) - Machine learning library
- [Django](https://www.djangoproject.com/) - Web framework
- [Truffle](https://trufflesuite.com/) - Blockchain development framework
- [Web3.py](https://web3py.readthedocs.io/) - Ethereum Python library

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs
3. Open an issue on GitHub
4. Contact the development team

---

**⚠️ Disclaimer**: This is a proof-of-concept MVP. For production use, implement additional security measures, error handling, and testing.

#   a i - d e c e n t r a l i z e d - i d e n t i t y - v e r f i c a t i o n 
 
 
