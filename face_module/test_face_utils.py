"""
Unit tests for face_utils.py
"""
import unittest
import numpy as np
import hashlib
from face_utils import (
    encode_face, hash_face_encoding, verify_face, 
    compare_faces, get_face_distance, detect_faces_in_image,
    encode_all_faces
)


class TestFaceUtils(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a dummy face encoding for testing
        self.dummy_encoding = np.random.rand(128).astype(np.float32)
        self.dummy_hash = hash_face_encoding(self.dummy_encoding)
        
        # Create a test image (dummy bytes)
        self.test_image_bytes = b"dummy_image_data"
    
    def test_hash_face_encoding(self):
        """Test face encoding hashing"""
        # Test with valid encoding
        result = hash_face_encoding(self.dummy_encoding)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 64)  # SHA-256 hex length
        self.assertIsInstance(result, str)
        
        # Test that same encoding produces same hash
        result2 = hash_face_encoding(self.dummy_encoding)
        self.assertEqual(result, result2)
        
        # Test that different encodings produce different hashes
        different_encoding = np.random.rand(128).astype(np.float32)
        different_hash = hash_face_encoding(different_encoding)
        self.assertNotEqual(result, different_hash)
    
    def test_verify_face(self):
        """Test face verification"""
        # Test with matching face
        result = verify_face(self.dummy_encoding, self.dummy_hash)
        self.assertTrue(result)
        
        # Test with non-matching face
        different_encoding = np.random.rand(128).astype(np.float32)
        result = verify_face(different_encoding, self.dummy_hash)
        self.assertFalse(result)
        
        # Test with invalid hash
        result = verify_face(self.dummy_encoding, "invalid_hash")
        self.assertFalse(result)
    
    def test_compare_faces(self):
        """Test face comparison"""
        encoding1 = np.random.rand(128).astype(np.float32)
        encoding2 = np.random.rand(128).astype(np.float32)
        
        # Test with different encodings (should not match)
        result = compare_faces(encoding1, encoding2)
        self.assertFalse(result)
        
        # Test with same encoding (should match)
        result = compare_faces(encoding1, encoding1)
        self.assertTrue(result)
    
    def test_get_face_distance(self):
        """Test face distance calculation"""
        encoding1 = np.random.rand(128).astype(np.float32)
        encoding2 = np.random.rand(128).astype(np.float32)
        
        # Test distance calculation
        distance = get_face_distance(encoding1, encoding2)
        self.assertIsInstance(distance, float)
        self.assertGreaterEqual(distance, 0)
        
        # Test with same encoding (distance should be 0)
        distance_same = get_face_distance(encoding1, encoding1)
        self.assertEqual(distance_same, 0)
    
    def test_hash_face_encoding_edge_cases(self):
        """Test edge cases for face encoding hashing"""
        # Test with None input
        result = hash_face_encoding(None)
        self.assertIsNone(result)
        
        # Test with invalid input
        result = hash_face_encoding("invalid_input")
        self.assertIsNone(result)
    
    def test_verify_face_edge_cases(self):
        """Test edge cases for face verification"""
        # Test with None encoding
        result = verify_face(None, self.dummy_hash)
        self.assertFalse(result)
        
        # Test with None hash
        result = verify_face(self.dummy_encoding, None)
        self.assertFalse(result)
        
        # Test with empty string hash
        result = verify_face(self.dummy_encoding, "")
        self.assertFalse(result)
    
    def test_compare_faces_edge_cases(self):
        """Test edge cases for face comparison"""
        encoding = np.random.rand(128).astype(np.float32)
        
        # Test with None inputs
        result = compare_faces(None, encoding)
        self.assertFalse(result)
        
        result = compare_faces(encoding, None)
        self.assertFalse(result)
        
        result = compare_faces(None, None)
        self.assertFalse(result)
    
    def test_get_face_distance_edge_cases(self):
        """Test edge cases for face distance calculation"""
        encoding = np.random.rand(128).astype(np.float32)
        
        # Test with None inputs
        distance = get_face_distance(None, encoding)
        self.assertEqual(distance, float('inf'))
        
        distance = get_face_distance(encoding, None)
        self.assertEqual(distance, float('inf'))
        
        distance = get_face_distance(None, None)
        self.assertEqual(distance, float('inf'))
    
    def test_detect_faces_in_image_edge_cases(self):
        """Test edge cases for face detection"""
        # Test with None input
        result = detect_faces_in_image(None)
        self.assertEqual(result, [])
        
        # Test with empty bytes
        result = detect_faces_in_image(b"")
        self.assertEqual(result, [])
        
        # Test with invalid image data
        result = detect_faces_in_image(b"invalid_image_data")
        self.assertEqual(result, [])
    
    def test_encode_all_faces_edge_cases(self):
        """Test edge cases for encoding all faces"""
        # Test with None input
        result = encode_all_faces(None)
        self.assertEqual(result, [])
        
        # Test with empty bytes
        result = encode_all_faces(b"")
        self.assertEqual(result, [])
        
        # Test with invalid image data
        result = encode_all_faces(b"invalid_image_data")
        self.assertEqual(result, [])


class TestFaceUtilsIntegration(unittest.TestCase):
    """Integration tests for face utilities"""
    
    def test_full_workflow(self):
        """Test the complete workflow from encoding to verification"""
        # This test would require actual face images
        # For now, we'll test the workflow with dummy data
        
        # Create dummy encoding
        encoding = np.random.rand(128).astype(np.float32)
        
        # Hash the encoding
        face_hash = hash_face_encoding(encoding)
        self.assertIsNotNone(face_hash)
        
        # Verify the face
        result = verify_face(encoding, face_hash)
        self.assertTrue(result)
        
        # Test with different encoding
        different_encoding = np.random.rand(128).astype(np.float32)
        result = verify_face(different_encoding, face_hash)
        self.assertFalse(result)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
