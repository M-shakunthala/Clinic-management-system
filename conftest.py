"""
Pytest configuration file for Clinic Management System
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """Create a test client"""
    return TestClient(app)

@pytest.fixture
def test_user_data():
    """Test user data for testing"""
    return {
        "email": "pytest_user@test.com",
        "password": "testpass123",
        "full_name": "Test User",
        "role": "patient"
    }

@pytest.fixture
def admin_credentials():
    """Admin credentials for testing"""
    return {
        "email": "admin@hospital.com",
        "password": "admin123"
    }

@pytest.fixture
def doctor_credentials():
    """Doctor credentials for testing"""
    return {
        "email": "doctor@hospital.com", 
        "password": "doctor123"
    }

@pytest.fixture
def patient_credentials():
    """Patient credentials for testing"""
    return {
        "email": "patient@hospital.com",
        "password": "patient123"
    }
