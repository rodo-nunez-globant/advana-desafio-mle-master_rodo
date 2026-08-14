"""Tests for API coverage"""

import pytest
from fastapi.testclient import TestClient
from challenge.api import app


class TestAPICoverage:
    """Test API endpoints for complete coverage"""
    
    def setup_method(self):
        """Setup test client"""
        self.client = TestClient(app)
    
    def test_health_endpoint(self):
        """Test the /health endpoint"""
        response = self.client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "OK"}
    
    def test_predict_endpoint(self):
        """Test the /predict endpoint (even though it's not implemented)"""
        response = self.client.post("/predict")
        assert response.status_code == 200
        assert response.json() == {"message": "Predict endpoint not yet implemented"}