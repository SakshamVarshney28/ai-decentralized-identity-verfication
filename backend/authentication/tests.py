from django.test import TestCase
from django.urls import reverse
import json
import base64
import hashlib

class AuthenticationAPITestCase(TestCase):
    """Test cases for authentication API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.register_url = reverse('register')
        self.verify_url = reverse('verify')
        
        # Create a dummy base64 image for testing
        dummy_image_data = b"dummy_image_data_for_testing"
        self.dummy_image_b64 = base64.b64encode(dummy_image_data).decode('utf-8')
    
    def test_register_missing_fields(self):
        """Test registration with missing fields"""
        response = self.client.post(
            self.register_url,
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
    
    def test_register_invalid_json(self):
        """Test registration with invalid JSON"""
        response = self.client.post(
            self.register_url,
            data="invalid json",
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    
    def test_verify_missing_fields(self):
        """Test verification with missing fields"""
        response = self.client.post(
            self.verify_url,
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
    
    def test_verify_invalid_json(self):
        """Test verification with invalid JSON"""
        response = self.client.post(
            self.verify_url,
            data="invalid json",
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

