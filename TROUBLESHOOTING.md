# Troubleshooting "Network Error"

## ✅ Quick Checklist

### 1. **Is Django Server Running?**
```cmd
# Check if Django is running on port 8000
# You should see: "Starting development server at http://127.0.0.1:8000/"
```

**Fix:** Start Django server:
```cmd
cd backend
python manage.py runserver 8000
```

---

### 2. **Is Ganache Running?**
```cmd
# Check if Ganache is running on port 7545
# You should see Ganache output with accounts listed
```

**Fix:** Start Ganache:
```cmd
npx ganache --port 7545 --deterministic
```

---

### 3. **Is Contract Deployed?**
Check `backend/authentication/views.py` line 48 - contract address should be set.

**Fix:** Deploy contract:
```cmd
cd blockchain
npx truffle migrate --reset
# Copy the contract address and update views.py
```

---

### 4. **Frontend Opening Method**

**❌ Wrong:** Opening `index.html` directly (file:// protocol)
- CORS will block API calls
- Camera may not work

**✅ Correct:** Serve via HTTP server:
```cmd
# Option 1: Python HTTP server
cd frontend
python -m http.server 3000
# Then open: http://localhost:3000/index.html

# Option 2: Use Django to serve static files
# Add to Django settings and serve from Django
```

---

### 5. **Check Browser Console**

Open browser Developer Tools (F12) and check:
- **Console tab:** Look for JavaScript errors
- **Network tab:** Check if API calls are being made
- **CORS errors:** Should be fixed with updated settings

---

### 6. **Test API Directly**

Test if Django API is accessible:
```cmd
# Test register endpoint
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test","face_image":"test"}'
```

---

### 7. **Check Django Logs**

When you start Django, you should see:
```
✅ Connected to Ganache blockchain
Contract initialized at address: 0x...
```

If you see errors, fix them first.

---

### 8. **Verify Web3 Connection**

In Django shell:
```cmd
cd backend
python manage.py shell
```

Then:
```python
from authentication.views import w3, contract
print("Connected:", w3.is_connected())
print("Contract:", contract)
```

---

## 🔧 Common Fixes

### Fix 1: Restart Everything
1. Stop Django (Ctrl+C)
2. Stop Ganache (Ctrl+C)
3. Restart Ganache
4. Restart Django
5. Refresh browser

### Fix 2: Clear Browser Cache
- Press Ctrl+Shift+Delete
- Clear cache and cookies
- Refresh page

### Fix 3: Check Firewall
- Windows Firewall might be blocking connections
- Allow Python and Node.js through firewall

### Fix 4: Use Correct URL
- Frontend should call: `http://127.0.0.1:8000/api/register/`
- Not: `http://localhost:8000/api/register/` (might have issues)
- Not: `/api/register/` (relative URL won't work from file://)

---

## 🐛 Debug Steps

1. **Check Django is running:**
   ```cmd
   # Should see Django welcome page
   curl http://127.0.0.1:8000/
   ```

2. **Check API endpoint:**
   ```cmd
   # Should return error (but not connection error)
   curl http://127.0.0.1:8000/api/register/
   ```

3. **Check Ganache:**
   ```cmd
   # Should return JSON
   curl http://127.0.0.1:7545
   ```

4. **Check browser console:**
   - Open DevTools (F12)
   - Look for network errors
   - Check if requests are being sent

---

## ✅ Expected Behavior

When everything works:
1. Django shows: "✅ Connected to Ganache blockchain"
2. Browser can make API calls (check Network tab)
3. No CORS errors in console
4. Registration/login works

---

## 📞 Still Having Issues?

1. Check all terminal windows are open
2. Verify all services are running
3. Check browser console for specific errors
4. Share the exact error message for help

