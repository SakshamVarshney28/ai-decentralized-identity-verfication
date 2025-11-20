#!/usr/bin/env python
"""
Quick script to check registered users on blockchain
Run: python check_users.py
"""

import sys
import os

# Add Django to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'faceauth_backend.settings')

import django
django.setup()

from authentication.views import contract, w3, CONTRACT_ADDRESS, verify_contract_deployed
from authentication.models import UserFaceEncoding

def check_users():
    print("=" * 60)
    print("FaceAuth - User Registration Checker")
    print("=" * 60)
    print()
    
    # Check Web3 connection
    print("1. Checking Web3 connection...")
    if w3.is_connected():
        print("   ✅ Connected to Ganache")
    else:
        print("   ❌ Not connected to Ganache")
        print("   💡 Start Ganache: npx ganache --port 7545")
        return
    print()
    
    # Check contract
    print("2. Checking contract...")
    print(f"   Contract address: {CONTRACT_ADDRESS}")
    is_deployed, message = verify_contract_deployed(CONTRACT_ADDRESS)
    if is_deployed:
        print(f"   ✅ Contract deployed: {message}")
    else:
        print(f"   ❌ Contract not deployed: {message}")
        print("   💡 Deploy contract: cd blockchain && npx truffle migrate")
        return
    print()
    
    # Check local database
    print("3. Checking local database...")
    local_users = UserFaceEncoding.objects.all()
    print(f"   Found {local_users.count()} users in local database:")
    for user in local_users:
        print(f"   - {user.username} (created: {user.created_at})")
    print()
    
    # Check blockchain
    print("4. Checking blockchain...")
    if contract:
        # Test with usernames from local database
        if local_users.exists():
            print("   Checking users from local database on blockchain:")
            for user in local_users:
                try:
                    is_registered = contract.functions.isRegistered(user.username).call()
                    status = "✅ Registered" if is_registered else "❌ Not registered"
                    print(f"   - {user.username}: {status}")
                except Exception as e:
                    print(f"   - {user.username}: ❌ Error - {e}")
        else:
            print("   No users in local database to check")
            print("   💡 Register a user first")
    else:
        print("   ❌ Contract not initialized")
    print()
    
    # Instructions
    print("=" * 60)
    print("Instructions:")
    print("=" * 60)
    print("If user shows '❌ Not registered' on blockchain:")
    print("  1. Make sure Ganache is running")
    print("  2. Make sure contract is deployed")
    print("  3. Re-register the user")
    print()
    print("If user shows '✅ Registered' but login fails:")
    print("  1. Check username matches exactly (case-sensitive)")
    print("  2. Check password is correct")
    print("  3. Check face is similar to registration")
    print()

if __name__ == "__main__":
    check_users()

