# Debugging Registration Errors

## ✅ What I Fixed

1. **Better Error Messages** - Frontend now shows actual error from server
2. **Detailed Logging** - Django console shows step-by-step what's happening
3. **Better Error Handling** - Each step is checked and logged

---

## 🔍 How to Debug

### Step 1: Check Django Console

When you try to register, watch the Django terminal. You should see:

```
📝 Registration attempt for user: testuser
✅ Password hashed
✅ Face image decoded, size: 12345 bytes
🔍 Encoding face...
✅ Face encoded, shape: (128,)
✅ Face hashed: abc123...
📤 Registering on blockchain with account: 0x...
⏳ Waiting for transaction: 0x...
✅ Transaction confirmed: 1
```

**If you see errors (❌), that's where the problem is!**

---

## 🐛 Common Issues & Solutions

### Issue 1: "Contract not initialized"
**Solution:**
- Check `backend/authentication/views.py` line 57
- Make sure `CONTRACT_ADDRESS` is set correctly
- Restart Django server after changing it

### Issue 2: "Web3 not connected"
**Solution:**
- Make sure Ganache is running: `npx ganache --port 7545`
- Check if you see "✅ Connected to Ganache blockchain" when Django starts

### Issue 3: "No face detected"
**Solution:**
- Make sure face_recognition is installed: `pip install face_recognition`
- Ensure good lighting
- Face should be clearly visible in camera

### Issue 4: "Face encoding failed"
**Solution:**
- Check if dlib is installed: `pip install dlib`
- On Windows, may need Visual Studio Build Tools
- Check Django console for full error traceback

### Issue 5: "Blockchain registration failed"
**Solution:**
- Check Ganache is running
- Verify contract address is correct
- Check if account has enough balance (Ganache gives free ETH)
- Look at full error in Django console

---

## 📋 Quick Checklist

Before registering, verify:

- [ ] Ganache is running (check terminal)
- [ ] Django server is running (check terminal)
- [ ] Contract address is set in `views.py`
- [ ] You see "✅ Connected to Ganache blockchain" in Django startup
- [ ] You see "Contract initialized at address: 0x..." in Django startup
- [ ] face_recognition is installed
- [ ] Camera permissions are granted
- [ ] Face is clearly visible when capturing

---

## 🔧 Test Each Component

### Test 1: Web3 Connection
```python
# In Django shell: python manage.py shell
from authentication.views import w3
print("Connected:", w3.is_connected())
print("Accounts:", w3.eth.accounts)
```

### Test 2: Contract
```python
# In Django shell
from authentication.views import contract, CONTRACT_ADDRESS
print("Contract address:", CONTRACT_ADDRESS)
print("Contract object:", contract)
```

### Test 3: Face Recognition
```python
# In Python shell
from face_module.face_utils import encode_face
# This should not error
print("Face utils imported successfully")
```

---

## 📊 What to Look For

When registration fails, check Django console for:

1. **Which step failed?** (Password hash, face decode, face encode, blockchain)
2. **What's the exact error?** (Copy the full traceback)
3. **Is the contract initialized?** (Should see message at startup)

---

## 💡 Next Steps

1. **Restart Django server** to see new logging
2. **Try registration again**
3. **Check Django console** for detailed error messages
4. **Share the error message** you see in the browser AND Django console

The error message in the browser should now be much more helpful!

