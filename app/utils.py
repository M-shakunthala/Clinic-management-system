from passlib.context import CryptContext
import hashlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    # Ensure password is not too long for bcrypt (72 bytes max)
    if len(password.encode('utf-8')) > 72:
        password = password[:72]
    
    try:
        return pwd_context.hash(password)
    except ValueError as e:
        if "72 bytes" in str(e):
            # Fallback to SHA256 for problematic passwords
            return hashlib.sha256(password.encode()).hexdigest()
        raise e

def verify_password(plain: str, hashed: str):
    # Check if it's a SHA256 hash (64 characters) for demo users
    if len(hashed) == 64:
        return hashlib.sha256(plain.encode()).hexdigest() == hashed
    
    # Ensure password is not too long for bcrypt
    if len(plain.encode('utf-8')) > 72:
        plain = plain[:72]
    
    # Otherwise use bcrypt
    try:
        return pwd_context.verify(plain, hashed)
    except ValueError:
        # If bcrypt fails, try SHA256 fallback
        return hashlib.sha256(plain.encode()).hexdigest() == hashed
