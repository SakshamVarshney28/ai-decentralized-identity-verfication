# Fix: "no such table: user_face_encodings"

## 🔴 The Problem

Error: "no such table: user_face_encodings"

This means the database migration hasn't been run yet. The `UserFaceEncoding` model was added but the table wasn't created.

---

## ✅ Quick Fix

### Step 1: Create Migration

```cmd
# In venv terminal
cd backend
python manage.py makemigrations
```

You should see:
```
Migrations for 'authentication':
  authentication/migrations/0001_initial.py
    - Create model UserFaceEncoding
```

### Step 2: Apply Migration

```cmd
python manage.py migrate
```

You should see:
```
Running migrations:
  Applying authentication.0001_initial... OK
```

### Step 3: Restart Django

```cmd
# Stop Django (Ctrl+C)
# Then restart:
python manage.py runserver 8000
```

---

## ✅ That's It!

The table will be created and the error should be gone.

---

## 🔍 Verify It Worked

### Option 1: Check Django Console

When Django starts, you shouldn't see the table error anymore.

### Option 2: Check in Django Shell

```cmd
cd backend
python manage.py shell
```

Then:
```python
from authentication.models import UserFaceEncoding
# This should not error
print("Table exists!")
```

---

## 🐛 If Migration Fails

### Issue: "No changes detected"

**Fix:**
```cmd
# Make sure you're in the backend directory
cd backend
python manage.py makemigrations authentication
```

### Issue: "Migration already exists"

**Fix:**
```cmd
# Apply existing migrations
python manage.py migrate
```

### Issue: "Table already exists"

**Fix:**
```cmd
# Reset migrations (WARNING: This deletes data!)
python manage.py migrate authentication zero
python manage.py makemigrations
python manage.py migrate
```

---

## 📋 Quick Checklist

- [ ] Run `python manage.py makemigrations`
- [ ] Run `python manage.py migrate`
- [ ] Restart Django server
- [ ] Error should be gone

---

**Run the migrations and the error will be fixed!** 🚀

