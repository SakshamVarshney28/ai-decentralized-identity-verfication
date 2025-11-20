# Debug: User Not Found in Login

## 🔴 The Problem

Login says "User not found" even after registration.

## 🔍 Debugging Steps

### Step 1: Check Django Console

When you try to login, watch the Django terminal. You should see:

```
🔍 Login attempt for user: testuser
🔍 Checking if user 'testuser' exists on blockchain...
✅ isRegistered result: True/False
```

**If you see `False`, the user isn't registered on blockchain!**

---

### Step 2: Verify User is Registered

#### Option A: Check in Django Shell

```cmd
# In venv terminal
cd backend
python manage.py shell
```

Then:
```python
from authentication.views import contract, w3, CONTRACT_ADDRESS

# Check contract
print("Contract address:", CONTRACT_ADDRESS)
print("Contract object:", contract)

# Check if user exists
username = "testuser"  # Your username
is_registered = contract.functions.isRegistered(username).call()
print(f"User '{username}' registered: {is_registered}")

# If registered, get user data
if is_registered:
    user_data = contract.functions.getUserHash(username).call()
    print("User data:", user_data)
```

#### Option B: Check Local Database

```python
from authentication.models import UserFaceEncoding

# Check local database
users = UserFaceEncoding.objects.all()
for user in users:
    print(f"Username: {user.username}, Created: {user.created_at}")
```

---

### Step 3: Common Issues & Fixes

#### Issue 1: User exists locally but not on blockchain

**Symptoms:**
- Django console shows: "⚠️ User exists in local database but not on blockchain!"

**Cause:** Registration failed at blockchain step

**Fix:**
1. Check if Ganache is running
2. Check if contract is deployed
3. Re-register the user

---

#### Issue 2: Username mismatch

**Symptoms:**
- Registered with "TestUser" but logging in with "testuser"

**Cause:** Usernames are case-sensitive

**Fix:**
- Use exact same username (case-sensitive)

---

#### Issue 3: Ganache was reset

**Symptoms:**
- User was registered, but after restarting Ganache, user is gone

**Cause:** Ganache data was lost

**Fix:**
- Use `--deterministic` flag: `npx ganache --port 7545 --deterministic`
- Re-register users

---

#### Issue 4: Contract address changed

**Symptoms:**
- Registration worked, but login fails

**Cause:** Contract was redeployed with new address

**Fix:**
1. Get new contract address from `truffle migrate`
2. Update `views.py` line 58
3. Restart Django

---

### Step 4: Verify Registration Completed

Check Django console during registration. You should see:

```
📝 Registration attempt for user: testuser
✅ Password hashed
✅ Face image decoded
✅ Face encoded
✅ Face hashed
✅ Face encoding stored locally
📤 Registering on blockchain...
⏳ Waiting for transaction: 0x...
✅ Transaction confirmed: 1
```

**If you see "❌ Blockchain registration error", registration didn't complete!**

---

## 🔧 Quick Fixes

### Fix 1: Re-register User

1. Make sure Ganache is running
2. Make sure contract is deployed
3. Register user again
4. Check Django console for success message
5. Try login again

### Fix 2: Check Username Exactly

Make sure you're using the **exact same username** (case-sensitive, no extra spaces):

```python
# In Django shell
from authentication.views import contract

# List all registered users (if contract supports it)
# Or check manually:
username = "testuser"  # Your exact username
print(contract.functions.isRegistered(username).call())
```

### Fix 3: Verify Contract

```python
# In Django shell
from authentication.views import contract, CONTRACT_ADDRESS, verify_contract_deployed

is_deployed, message = verify_contract_deployed(CONTRACT_ADDRESS)
print(f"Contract deployed: {is_deployed}, Message: {message}")
print(f"Contract object: {contract}")
```

---

## 📋 Checklist

Before trying to login, verify:

- [ ] User was registered successfully (check Django console)
- [ ] Registration showed "✅ Transaction confirmed"
- [ ] Ganache is still running (same instance)
- [ ] Contract address hasn't changed
- [ ] Username matches exactly (case-sensitive)
- [ ] No extra spaces in username

---

## 🎯 Expected Behavior

**Successful Registration:**
```
✅ Transaction confirmed: 1
```

**Successful Login Check:**
```
🔍 Checking if user 'testuser' exists on blockchain...
✅ isRegistered result: True
```

**Failed Login Check:**
```
🔍 Checking if user 'testuser' exists on blockchain...
✅ isRegistered result: False
❌ User not found in blockchain or local database
```

---

## 💡 Pro Tip

**Always check Django console** - it shows exactly what's happening at each step!

If `isRegistered` returns `False`, the user wasn't registered on blockchain. Re-register!

