"""
Face recognition utilities for encoding, hashing, and verification
"""
try:
    import face_recognition
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    FACE_RECOGNITION_AVAILABLE = False
    print("Warning: face_recognition not installed. Install with: pip install face_recognition")

import numpy as np
import hashlib
import cv2
from PIL import Image
import io


def encode_face(image_bytes):
    """
    Encode a face from image bytes into a 128-dimensional face encoding
    
    Args:
        image_bytes: Raw image bytes
        
    Returns:
        numpy array: 128-dimensional face encoding or None if no face found
    """
    if not FACE_RECOGNITION_AVAILABLE:
        print("Error: face_recognition not available")
        return None
    
    try:
        # Convert bytes to PIL Image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert PIL to RGB (face_recognition expects RGB)
        rgb_image = image.convert('RGB')
        
        # Convert to numpy array
        image_array = np.array(rgb_image)
        
        # Find face locations
        face_locations = face_recognition.face_locations(image_array)
        
        if not face_locations:
            return None
        
        # Get face encodings (128-dimensional vectors)
        face_encodings = face_recognition.face_encodings(image_array, face_locations)
        
        if not face_encodings:
            return None
        
        # Return the first face encoding
        return face_encodings[0]
        
    except Exception as e:
        print(f"Error encoding face: {e}")
        return None


def hash_face_encoding(face_encoding):
    """
    Convert a face encoding to SHA-256 hash
    
    Args:
        face_encoding: numpy array of face encoding
        
    Returns:
        str: SHA-256 hash of the face encoding
    """
    try:
        # Convert numpy array to bytes
        encoding_bytes = face_encoding.tobytes()
        
        # Create SHA-256 hash
        hash_object = hashlib.sha256(encoding_bytes)
        return hash_object.hexdigest()
        
    except Exception as e:
        print(f"Error hashing face encoding: {e}")
        return None


def verify_face(current_encoding, stored_hash):
    """
    Verify if current face encoding matches stored hash
    
    Args:
        current_encoding: numpy array of current face encoding
        stored_hash: stored hash string
        
    Returns:
        bool: True if face matches, False otherwise
    """
    try:
        # Hash the current encoding
        current_hash = hash_face_encoding(current_encoding)
        
        if current_hash is None:
            return False
        
        # Compare hashes
        return current_hash == stored_hash
        
    except Exception as e:
        print(f"Error verifying face: {e}")
        return False


def compare_faces(encoding1, encoding2, tolerance=0.6):
    """
    Compare two face encodings using face_recognition library
    
    Args:
        encoding1: First face encoding
        encoding2: Second face encoding
        tolerance: Distance tolerance (lower = more strict)
        
    Returns:
        bool: True if faces match, False otherwise
    """
    try:
        # Use face_recognition's compare_faces function
        results = face_recognition.compare_faces([encoding1], encoding2, tolerance=tolerance)
        return results[0] if results else False
        
    except Exception as e:
        print(f"Error comparing faces: {e}")
        return False


def get_face_distance(encoding1, encoding2):
    """
    Get the distance between two face encodings
    
    Args:
        encoding1: First face encoding
        encoding2: Second face encoding
        
    Returns:
        float: Distance between encodings (lower = more similar)
    """
    try:
        # Use face_recognition's face_distance function
        distances = face_recognition.face_distance([encoding1], encoding2)
        return distances[0] if len(distances) > 0 else float('inf')
        
    except Exception as e:
        print(f"Error calculating face distance: {e}")
        return float('inf')


def detect_faces_in_image(image_bytes):
    """
    Detect all faces in an image and return their locations
    
    Args:
        image_bytes: Raw image bytes
        
    Returns:
        list: List of face locations (top, right, bottom, left)
    """
    try:
        # Convert bytes to PIL Image
        image = Image.open(io.BytesIO(image_bytes))
        rgb_image = image.convert('RGB')
        image_array = np.array(rgb_image)
        
        # Find face locations
        face_locations = face_recognition.face_locations(image_array)
        return face_locations
        
    except Exception as e:
        print(f"Error detecting faces: {e}")
        return []


def encode_all_faces(image_bytes):
    """
    Encode all faces found in an image
    
    Args:
        image_bytes: Raw image bytes
        
    Returns:
        list: List of face encodings
    """
    try:
        # Convert bytes to PIL Image
        image = Image.open(io.BytesIO(image_bytes))
        rgb_image = image.convert('RGB')
        image_array = np.array(rgb_image)
        
        # Find face locations
        face_locations = face_recognition.face_locations(image_array)
        
        if not face_locations:
            return []
        
        # Get face encodings
        face_encodings = face_recognition.face_encodings(image_array, face_locations)
        return face_encodings
        
    except Exception as e:
        print(f"Error encoding all faces: {e}")
        return []
