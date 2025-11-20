import json
import hashlib
import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from web3 import Web3
import sys
import os

# Add the face_module to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from face_module.face_utils import encode_face, hash_face_encoding, verify_face, compare_faces
from .models import UserFaceEncoding

# Initialize Web3 connection to Ganache
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

# Check Web3 connection
try:
    if w3.is_connected():
        print("✅ Connected to Ganache blockchain")
    else:
        print("❌ Not connected to Ganache. Make sure Ganache is running on port 7545")
except Exception as e:
    print(f"❌ Error connecting to Ganache: {e}")

# Contract ABI and address (will be set after deployment)
CONTRACT_ABI = [
    {
        "inputs": [
            {"internalType": "string", "name": "username", "type": "string"},
            {"internalType": "string", "name": "passwordHash", "type": "string"},
            {"internalType": "string", "name": "faceHash", "type": "string"}
        ],
        "name": "registerUser",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "string", "name": "username", "type": "string"}],
        "name": "getUserHash",
        "outputs": [
            {"internalType": "string", "name": "passwordHash", "type": "string"},
            {"internalType": "string", "name": "faceHash", "type": "string"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "string", "name": "username", "type": "string"}],
        "name": "isRegistered",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    }
]

# Contract address (to be set after deployment)
CONTRACT_ADDRESS = "0xe78A0F7E598Cc8b0Bb87894B0F60dD2a88d6a8Ab"
contract = None

def verify_contract_deployed(address):
    """Verify that a contract is actually deployed at the given address"""
    try:
        if not w3.is_connected():
            return False, "Not connected to blockchain"
        
        # Check if address is valid
        if not w3.is_address(address):
            return False, "Invalid address format"
        
        # Check if contract has code (is deployed)
        code = w3.eth.get_code(address)
        if code == b'':
            return False, "No contract code found at this address"
        
        return True, "Contract verified"
    except Exception as e:
        return False, f"Error verifying contract: {str(e)}"

# Initialize contract if address is set
if CONTRACT_ADDRESS:
    try:
        # Verify contract is deployed
        is_deployed, message = verify_contract_deployed(CONTRACT_ADDRESS)
        if is_deployed:
            contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
            print(f"✅ Contract initialized and verified at address: {CONTRACT_ADDRESS}")
        else:
            print(f"❌ Contract not deployed: {message}")
            print(f"   Address: {CONTRACT_ADDRESS}")
            print(f"   Please deploy the contract using: cd blockchain && npx truffle migrate")
    except Exception as e:
        print(f"❌ Warning: Could not initialize contract: {e}")

def set_contract_address(address):
    """Set the contract address after deployment"""
    global CONTRACT_ADDRESS, contract
    CONTRACT_ADDRESS = address
    if CONTRACT_ADDRESS:
        contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    """
    Register a new user with username, password, and face image
    """
    try:
        # Parse request data
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error: {e}")
            return JsonResponse({'error': f'Invalid JSON: {str(e)}'}, status=400)
        
        username = data.get('username')
        password = data.get('password')
        face_image_data = data.get('face_image')  # Base64 encoded image
        
        print(f"📝 Registration attempt for user: {username}")
        
        if not all([username, password, face_image_data]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        # Check Web3 connection
        if not w3.is_connected():
            print("❌ Web3 not connected")
            return JsonResponse({'error': 'Blockchain not connected. Is Ganache running?'}, status=500)
        
        # Check contract initialization
        if not contract:
            print("❌ Contract not initialized")
            return JsonResponse({
                'error': 'Contract not deployed. Please deploy the contract first using: cd blockchain && npx truffle migrate'
            }, status=500)
        
        # Verify contract is still deployed
        is_deployed, message = verify_contract_deployed(CONTRACT_ADDRESS)
        if not is_deployed:
            print(f"❌ Contract verification failed: {message}")
            return JsonResponse({
                'error': f'Contract not found at address {CONTRACT_ADDRESS}. Please deploy the contract first.'
            }, status=500)
        
        # Check if user already exists
        try:
            if contract.functions.isRegistered(username).call():
                return JsonResponse({'error': 'User already exists'}, status=400)
        except Exception as e:
            print(f"❌ Error checking user existence: {e}")
            error_msg = str(e)
            if "contract" in error_msg.lower() and "deployed" in error_msg.lower():
                return JsonResponse({
                    'error': 'Contract not deployed correctly. Please run: cd blockchain && npx truffle migrate --reset'
                }, status=500)
            return JsonResponse({'error': f'Error checking user: {error_msg}'}, status=500)
        
        # Hash password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        print(f"✅ Password hashed")
        
        # Process face image
        try:
            face_image_bytes = base64.b64decode(face_image_data)
            print(f"✅ Face image decoded, size: {len(face_image_bytes)} bytes")
        except Exception as e:
            print(f"❌ Base64 decode error: {e}")
            return JsonResponse({'error': f'Invalid image data: {str(e)}'}, status=400)
        
        # Encode face and get hash
        print("🔍 Encoding face...")
        try:
            face_encoding = encode_face(face_image_bytes)
            if face_encoding is None:
                print("❌ No face detected")
                return JsonResponse({'error': 'No face detected in image. Please ensure your face is clearly visible.'}, status=400)
            print(f"✅ Face encoded, shape: {face_encoding.shape}")
        except Exception as e:
            print(f"❌ Face encoding error: {e}")
            import traceback
            traceback.print_exc()
            return JsonResponse({'error': f'Face encoding failed: {str(e)}'}, status=500)
        
        face_hash = hash_face_encoding(face_encoding)
        if not face_hash:
            return JsonResponse({'error': 'Face hashing failed'}, status=500)
        print(f"✅ Face hashed: {face_hash[:16]}...")
        
        # Validate all inputs before sending to blockchain
        if not username or len(username.strip()) == 0:
            return JsonResponse({'error': 'Username cannot be empty'}, status=400)
        if not password_hash or len(password_hash) != 64:  # SHA-256 hex is 64 chars
            return JsonResponse({'error': 'Invalid password hash'}, status=400)
        if not face_hash or len(face_hash) != 64:  # SHA-256 hex is 64 chars
            return JsonResponse({'error': 'Invalid face hash'}, status=400)
        
        print(f"📋 Registration data:")
        print(f"   Username: '{username}' (length: {len(username)})")
        print(f"   Password hash: {password_hash[:16]}... (length: {len(password_hash)})")
        print(f"   Face hash: {face_hash[:16]}... (length: {len(face_hash)})")
        
        # Register on blockchain FIRST (before storing locally)
        try:
            # Get account for transaction
            accounts = w3.eth.accounts
            if not accounts:
                return JsonResponse({'error': 'No accounts available'}, status=500)
            
            account = accounts[0]
            print(f"📤 Registering on blockchain with account: {account}")
            
            # Check account balance
            balance = w3.eth.get_balance(account)
            print(f"💰 Account balance: {w3.from_wei(balance, 'ether')} ETH")
            
            if balance == 0:
                return JsonResponse({'error': 'Account has no balance. Check Ganache accounts.'}, status=500)
            
            # Estimate gas first
            try:
                gas_estimate = contract.functions.registerUser(
                    username.strip(), 
                    password_hash, 
                    face_hash
                ).estimate_gas({'from': account})
                print(f"⛽ Estimated gas: {gas_estimate}")
                gas_limit = int(gas_estimate * 1.2)  # Add 20% buffer
            except Exception as e:
                print(f"⚠️ Gas estimation failed: {e}")
                gas_limit = 300000  # Use default if estimation fails
            
            # Build transaction with validated inputs
            tx = contract.functions.registerUser(
                username.strip(),  # Ensure no leading/trailing spaces
                password_hash,
                face_hash
            ).build_transaction({
                'from': account,
                'gas': gas_limit,
                'gasPrice': w3.eth.gas_price,
                'nonce': w3.eth.get_transaction_count(account)
            })
            
            print(f"📝 Transaction details:")
            print(f"   Gas limit: {gas_limit}")
            print(f"   Gas price: {w3.eth.gas_price}")
            print(f"   Nonce: {tx['nonce']}")
            
            # Send transaction
            tx_hash = w3.eth.send_transaction(tx)
            print(f"⏳ Waiting for transaction: {tx_hash.hex()}")
            
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            
            # Check transaction status (1 = success, 0 = failed)
            if receipt.status != 1:
                print(f"❌ Transaction failed with status: {receipt.status}")
                print(f"   Transaction hash: {tx_hash.hex()}")
                print(f"   Gas used: {receipt.gasUsed}")
                print(f"   Block number: {receipt.blockNumber}")
                
                # Try to get revert reason using trace
                try:
                    # Try to call the function directly to see the error
                    print("🔍 Attempting to call function directly to see error...")
                    contract.functions.registerUser(username.strip(), password_hash, face_hash).call({'from': account})
                except Exception as call_error:
                    print(f"❌ Direct call error (this is the revert reason): {call_error}")
                    error_msg = str(call_error)
                    if "User already exists" in error_msg:
                        return JsonResponse({'error': 'User already exists on blockchain'}, status=400)
                    elif "cannot be empty" in error_msg:
                        return JsonResponse({'error': f'Validation error: {error_msg}'}, status=400)
                    else:
                        return JsonResponse({
                            'error': f'Transaction reverted: {error_msg}. Check Ganache logs for more details.'
                        }, status=500)
                
                return JsonResponse({
                    'error': f'Transaction failed on blockchain. Status: {receipt.status}. Check Ganache console for revert reason.'
                }, status=500)
            
            print(f"✅ Transaction confirmed with status: {receipt.status}")
            
            # Check transaction logs for events
            if receipt.logs:
                print(f"✅ Transaction emitted {len(receipt.logs)} events")
            else:
                print(f"⚠️ No events emitted (might be normal)")
            
            # Small delay to ensure state is updated
            import time
            time.sleep(0.5)
            
            # Verify user is now registered on blockchain
            try:
                is_registered = contract.functions.isRegistered(username).call()
                print(f"🔍 Verification check: isRegistered('{username}') = {is_registered}")
                
                if not is_registered:
                    # Try to get user data directly to see what's stored
                    try:
                        user_data = contract.functions.getUserHash(username).call()
                        print(f"⚠️ User data exists: {user_data}")
                    except Exception as e:
                        print(f"❌ Cannot get user data: {e}")
                    
                    # Additional debugging - check if it's a timing issue
                    print(f"⚠️ Waiting a bit longer and retrying...")
                    time.sleep(1)
                    is_registered_retry = contract.functions.isRegistered(username).call()
                    print(f"🔍 Retry check: isRegistered('{username}') = {is_registered_retry}")
                    
                    print("❌ User registration failed - not found on blockchain after transaction")
                    return JsonResponse({
                        'error': 'Registration transaction succeeded but user not found. This might be a contract issue. Check Ganache logs.'
                    }, status=500)
                
                print(f"✅ User verified on blockchain")
            except Exception as e:
                print(f"❌ Error verifying user: {e}")
                import traceback
                traceback.print_exc()
                return JsonResponse({
                    'error': f'Error verifying registration: {str(e)}'
                }, status=500)
            
        except Exception as e:
            print(f"❌ Blockchain registration error: {e}")
            import traceback
            traceback.print_exc()
            # Clean up: remove local data if it exists (from previous failed attempt)
            try:
                UserFaceEncoding.objects.filter(username=username).delete()
            except:
                pass
            return JsonResponse({'error': f'Blockchain registration failed: {str(e)}'}, status=500)
        
        # Store face encoding locally AFTER blockchain registration succeeds
        # (Face encodings vary slightly, so we can't use exact hash matching)
        try:
            face_encoding_obj, created = UserFaceEncoding.objects.get_or_create(
                username=username,
                defaults={'face_encoding': json.dumps(face_encoding.tolist())}
            )
            if not created:
                # Update existing encoding
                face_encoding_obj.set_encoding(face_encoding)
                face_encoding_obj.save()
            print(f"✅ Face encoding stored locally for similarity comparison")
        except Exception as e:
            print(f"⚠️ Warning: Could not store face encoding locally: {e}")
            # Continue anyway - we'll use hash comparison as fallback
        
        return JsonResponse({
            'success': True,
            'message': 'User registered successfully',
            'username': username,
            'password_hash': password_hash,
            'face_hash': face_hash
        })
            
    except Exception as e:
        print(f"❌ Unexpected error in register: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def verify(request):
    """
    Verify user login with username, password, and face image
    """
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        face_image_data = data.get('face_image')  # Base64 encoded image
        
        if not all([username, password, face_image_data]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        print(f"🔍 Login attempt for user: {username}")
        
        # Check Web3 connection
        if not w3.is_connected():
            print("❌ Web3 not connected")
            return JsonResponse({'error': 'Blockchain not connected. Is Ganache running?'}, status=500)
        
        # Check contract initialization
        if not contract:
            print("❌ Contract not initialized")
            return JsonResponse({
                'error': 'Contract not deployed. Please deploy the contract first using: cd blockchain && npx truffle migrate'
            }, status=500)
        
        # Verify contract is still deployed
        is_deployed, message = verify_contract_deployed(CONTRACT_ADDRESS)
        if not is_deployed:
            print(f"❌ Contract verification failed: {message}")
            return JsonResponse({
                'error': f'Contract not found at address {CONTRACT_ADDRESS}. Please deploy the contract first.'
            }, status=500)
        
        # Check if user exists
        print(f"🔍 Checking if user '{username}' exists on blockchain...")
        try:
            is_registered = contract.functions.isRegistered(username).call()
            print(f"✅ isRegistered result: {is_registered}")
            
            if not is_registered:
                # Also check if user exists in local database (orphaned data from failed registration)
                local_user = UserFaceEncoding.objects.filter(username=username).first()
                if local_user:
                    print(f"⚠️ User exists in local database but not on blockchain!")
                    print(f"   This means registration didn't complete successfully.")
                    print(f"   Cleaning up orphaned local data...")
                    # Clean up orphaned data
                    try:
                        local_user.delete()
                        print(f"✅ Cleaned up orphaned local data")
                    except Exception as e:
                        print(f"⚠️ Could not clean up: {e}")
                    return JsonResponse({
                        'error': 'User registration was incomplete. Please register again to complete the process.'
                    }, status=404)
                else:
                    print(f"❌ User not found in blockchain or local database")
                    return JsonResponse({
                        'error': f'User "{username}" not found. Please register first.'
                    }, status=404)
        except Exception as e:
            print(f"❌ Error checking user existence: {e}")
            import traceback
            traceback.print_exc()
            error_msg = str(e)
            if "contract" in error_msg.lower() and "deployed" in error_msg.lower():
                return JsonResponse({
                    'error': 'Contract not deployed correctly. Please run: cd blockchain && npx truffle migrate --reset'
                }, status=500)
            return JsonResponse({
                'error': f'Error checking user: {error_msg}'
            }, status=500)
        
        # Get stored data from blockchain
        print(f"🔍 Getting user data from blockchain...")
        try:
            stored_data = contract.functions.getUserHash(username).call()
            print(f"✅ Retrieved user data from blockchain")
            
            # getUserHash returns a tuple (passwordHash, faceHash)
            if isinstance(stored_data, tuple):
                stored_password_hash, stored_face_hash = stored_data
                print(f"✅ Parsed tuple: passwordHash length={len(stored_password_hash)}, faceHash length={len(stored_face_hash)}")
            elif isinstance(stored_data, list):
                # Handle list case (sometimes Web3 returns lists)
                if len(stored_data) == 2:
                    stored_password_hash, stored_face_hash = stored_data[0], stored_data[1]
                    print(f"✅ Parsed list: passwordHash length={len(stored_password_hash)}, faceHash length={len(stored_face_hash)}")
                else:
                    return JsonResponse({'error': f'Invalid user data format from blockchain: {stored_data}'}, status=500)
            elif isinstance(stored_data, str):
                # Fallback if it returns a string (shouldn't happen with correct ABI)
                if '|' in stored_data:
                    stored_password_hash, stored_face_hash = stored_data.split('|')
                    print(f"✅ Parsed string: passwordHash length={len(stored_password_hash)}, faceHash length={len(stored_face_hash)}")
                else:
                    return JsonResponse({'error': f'Invalid user data format from blockchain: {stored_data}'}, status=500)
            else:
                return JsonResponse({'error': f'Unexpected data type from blockchain: {type(stored_data)}'}, status=500)
        except Exception as e:
            print(f"❌ Error getting user data from blockchain: {e}")
            import traceback
            traceback.print_exc()
            return JsonResponse({'error': f'Error retrieving user data: {str(e)}'}, status=500)
        
        # Verify password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if password_hash != stored_password_hash:
            return JsonResponse({'error': 'Invalid password'}, status=401)
        
        # Process face image
        print("🔍 Processing face image for verification...")
        try:
            face_image_bytes = base64.b64decode(face_image_data)
            print(f"✅ Face image decoded, size: {len(face_image_bytes)} bytes")
        except Exception as e:
            print(f"❌ Base64 decode error: {e}")
            return JsonResponse({'error': f'Invalid image data: {str(e)}'}, status=400)
        
        print("🔍 Encoding face...")
        try:
            face_encoding = encode_face(face_image_bytes)
            if face_encoding is None:
                print("❌ No face detected")
                return JsonResponse({'error': 'No face detected in image. Please ensure your face is clearly visible.'}, status=400)
            print(f"✅ Face encoded, shape: {face_encoding.shape}")
        except Exception as e:
            print(f"❌ Face encoding error: {e}")
            import traceback
            traceback.print_exc()
            return JsonResponse({'error': f'Face encoding failed: {str(e)}'}, status=500)
        
        # Verify face using similarity comparison (not exact hash match)
        # Face encodings vary slightly, so we need to compare similarity
        print("🔍 Verifying face similarity...")
        face_match = False
        
        try:
            # Try to get stored face encoding from local database
            stored_encoding_obj = UserFaceEncoding.objects.filter(username=username).first()
            if stored_encoding_obj:
                stored_encoding = stored_encoding_obj.get_encoding()
                # Use face_recognition's compare_faces for similarity
                face_match = compare_faces(stored_encoding, face_encoding, tolerance=0.6)
                print(f"✅ Face similarity check: {'MATCH' if face_match else 'NO MATCH'}")
            else:
                # Fallback to hash comparison (less reliable)
                print("⚠️ No stored encoding found, using hash comparison (less reliable)")
                current_face_hash = hash_face_encoding(face_encoding)
                face_match = (current_face_hash == stored_face_hash)
                print(f"✅ Hash comparison: {'MATCH' if face_match else 'NO MATCH'}")
        except Exception as e:
            print(f"❌ Face verification error: {e}")
            import traceback
            traceback.print_exc()
            # Fallback to hash comparison
            current_face_hash = hash_face_encoding(face_encoding)
            face_match = (current_face_hash == stored_face_hash)
        
        if not face_match:
            print("❌ Face verification failed - faces don't match")
            return JsonResponse({
                'error': 'Face verification failed. Please ensure you are using the same face as registration.'
            }, status=401)
        
        print("✅ Face verification successful!")
        
        # Return dashboard data
        return JsonResponse({
            'success': True,
            'message': 'Login successful',
            'dashboard_data': {
                'username': username,
                'password_hash': password_hash,
                'face_encoding': face_encoding.tolist(),  # Convert numpy array to list
                'face_hash': hash_face_encoding(face_encoding)
            }
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
