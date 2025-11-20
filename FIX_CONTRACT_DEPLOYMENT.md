# Fix: Contract Deployment Error

## 🔴 The Problem

Error: "Could not transact with/call contract function, is contract deployed correctly and chain synced?"

This means the contract address in `views.py` doesn't match the actual deployed contract.

---

## ✅ Solution: Deploy Contract and Update Address

### Step 1: Make Sure Ganache is Running

```cmd
# In a terminal (NO venv)
npx ganache --port 7545 --deterministic
```

**Keep this running!**

---

### Step 2: Deploy the Contract

```cmd
# In a NEW terminal (NO venv)
cd blockchain
npx truffle compile
npx truffle migrate --reset
```

**Look for output like this:**
```
2_deploy_faceauth.js
===================

   Deploying 'FaceAuth'
   --------------------
   > transaction hash:    0x...
   > contract address:    0x1234567890abcdef...  <-- COPY THIS ADDRESS!
   > block number:        1
   > block timestamp:     ...
   > account:             0x...
   > balance:             99.99...
   > gas used:            123456
   > gas price:           20 gwei
   > value sent:          0 ETH
   > total cost:          0.00246912 ETH
```

**📋 Copy the contract address!** (starts with `0x`)

---

### Step 3: Update Contract Address in views.py

1. Open `backend/authentication/views.py`
2. Find line 57:
   ```python
   CONTRACT_ADDRESS = "0xe78A0F7E598Cc8b0Bb87894B0F60dD2a88d6a8Ab"
   ```
3. Replace with your NEW contract address:
   ```python
   CONTRACT_ADDRESS = "0x1234567890abcdef..."  # Your actual address from Step 2
   ```

---

### Step 4: Restart Django Server

```cmd
# In venv terminal
# Stop Django (Ctrl+C)
# Then restart:
cd backend
python manage.py runserver 8000
```

**You should now see:**
```
✅ Connected to Ganache blockchain
✅ Contract initialized and verified at address: 0x...
```

If you see:
```
❌ Contract not deployed: No contract code found at this address
```

Then the address is wrong - go back to Step 2 and copy the correct address.

---

## 🔍 Verify Contract is Deployed

### Method 1: Check Django Startup

When Django starts, you should see:
```
✅ Contract initialized and verified at address: 0x...
```

If you see an error, the contract isn't deployed correctly.

### Method 2: Test in Django Shell

```cmd
# In venv
cd backend
python manage.py shell
```

Then:
```python
from authentication.views import contract, CONTRACT_ADDRESS, verify_contract_deployed

# Check address
print("Contract address:", CONTRACT_ADDRESS)

# Verify deployment
is_deployed, message = verify_contract_deployed(CONTRACT_ADDRESS)
print(f"Deployed: {is_deployed}, Message: {message}")

# Check contract object
print("Contract object:", contract)
```

---

## 🐛 Common Issues

### Issue 1: "No contract code found"

**Cause:** Contract address is wrong or contract not deployed

**Fix:**
1. Make sure Ganache is running
2. Run `npx truffle migrate --reset` again
3. Copy the NEW contract address
4. Update `views.py` with the new address
5. Restart Django

### Issue 2: "Not connected to blockchain"

**Cause:** Ganache is not running

**Fix:**
1. Start Ganache: `npx ganache --port 7545`
2. Restart Django server

### Issue 3: Contract address keeps changing

**Cause:** Ganache is resetting (not using `--deterministic`)

**Fix:**
- Always use: `npx ganache --port 7545 --deterministic`
- This keeps the same accounts and addresses

### Issue 4: "Invalid address format"

**Cause:** Contract address is malformed

**Fix:**
- Make sure address starts with `0x`
- Should be 42 characters: `0x` + 40 hex characters
- Example: `0x1234567890abcdef1234567890abcdef12345678`

---

## 📋 Quick Checklist

- [ ] Ganache is running (`npx ganache --port 7545 --deterministic`)
- [ ] Contract is deployed (`npx truffle migrate --reset`)
- [ ] Contract address copied from Truffle output
- [ ] Contract address updated in `views.py` line 57
- [ ] Django server restarted
- [ ] Django shows "✅ Contract initialized and verified"

---

## 🎯 One-Line Fix

If you just deployed and need to update:

1. Copy contract address from `truffle migrate` output
2. Update `backend/authentication/views.py` line 57
3. Restart Django

That's it! 🎉

---

## 💡 Pro Tip

After deploying, you can automatically get the contract address:

```cmd
cd blockchain
npx truffle migrate --reset | grep "contract address"
```

This will show just the contract address line.

