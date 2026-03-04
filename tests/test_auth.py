"""
Test authentication endpoints
"""
import pytest
from fastapi.testclient import TestClient


class TestAuth:
    """Test authentication functionality"""

    def test_root_endpoint(self, client: TestClient):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Clinic Management System API" in data["message"]

    def test_test_endpoint(self, client: TestClient):
        """Test the /test endpoint"""
        response = client.get("/test")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data

    def test_admin_login(self, client: TestClient, admin_credentials):
        """Test admin login"""
        response = client.post("/auth/login", data=admin_credentials)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_doctor_login(self, client: TestClient, doctor_credentials):
        """Test doctor login"""
        response = client.post("/auth/login", data=doctor_credentials)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_patient_login(self, client: TestClient, patient_credentials):
        """Test patient login"""
        response = client.post("/auth/login", data=patient_credentials)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_invalid_login(self, client: TestClient):
        """Test login with invalid credentials"""
        invalid_creds = {"email": "invalid@test.com", "password": "wrongpass"}
        response = client.post("/auth/login", data=invalid_creds)
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data

    def test_user_signup(self, client: TestClient, test_user_data):
        """Test user registration"""
        response = client.post("/auth/signup", json=test_user_data)
        # Could be 200 (success) or 400 (user already exists)
        assert response.status_code in [200, 400]
        
        if response.status_code == 200:
            data = response.json()
            assert "id" in data
            assert data["email"] == test_user_data["email"]
            assert data["role"] == test_user_data["role"]

    def test_get_current_user(self, client: TestClient, admin_credentials):
        """Test getting current user info with valid token"""
        # First login to get token
        login_response = client.post("/auth/login", data=admin_credentials)
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        
        # Use token to get user info
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/auth/me", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "email" in data
        assert data["email"] == admin_credentials["email"]

    def test_unauthorized_access(self, client: TestClient):
        """Test accessing protected endpoint without token"""
        response = client.get("/auth/me")
        assert response.status_code == 401

    def test_invalid_token(self, client: TestClient):
        """Test accessing protected endpoint with invalid token"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/auth/me", headers=headers)
        assert response.status_code == 401
