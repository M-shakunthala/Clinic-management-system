"""
Test database operations
"""
import pytest
from app.database import SessionLocal, get_db
from app.models import User
from app.utils import hash_password


class TestDatabase:
    """Test database functionality"""

    def test_database_connection(self):
        """Test database connection"""
        db = SessionLocal()
        try:
            # Try to query the database
            users = db.query(User).all()
            assert isinstance(users, list)
        finally:
            db.close()

    def test_user_creation(self):
        """Test user creation in database"""
        db = SessionLocal()
        try:
            # Check if demo users exist
            admin = db.query(User).filter(User.email == "admin@hospital.com").first()
            doctor = db.query(User).filter(User.email == "doctor@hospital.com").first()
            patient = db.query(User).filter(User.email == "patient@hospital.com").first()
            
            assert admin is not None
            assert doctor is not None  
            assert patient is not None
            
            assert admin.role == "admin"
            assert doctor.role == "doctor"
            assert patient.role == "patient"
        finally:
            db.close()

    def test_password_hashing(self):
        """Test password hashing utility"""
        password = "testpassword123"
        hashed = hash_password(password)
        
        assert hashed != password
        assert len(hashed) > 10
