from django.db import models
import json
import numpy as np

class UserFaceEncoding(models.Model):
    """
    Store face encodings locally for similarity comparison
    Face encodings vary slightly, so we can't use exact hash matching
    """
    username = models.CharField(max_length=100, unique=True, db_index=True)
    face_encoding = models.TextField()  # Store as JSON string
    created_at = models.DateTimeField(auto_now_add=True)
    
    def set_encoding(self, encoding):
        """Store numpy array as JSON string"""
        self.face_encoding = json.dumps(encoding.tolist())
    
    def get_encoding(self):
        """Retrieve numpy array from JSON string"""
        return np.array(json.loads(self.face_encoding))
    
    class Meta:
        db_table = 'user_face_encodings'

