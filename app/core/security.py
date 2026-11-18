from datetime import datetime, timedelta,timezone
import hashlib
import secrets
import  jwt

from pwdlib import PasswordHash
from app.core.config import settings

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    """Mengubah password menjadi hash"""
    return password_hash.hash(password)

def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """Memeriksa password apakah cocok dengan hash."""
    return password_hash.verify(
        plain_password,
        hash_password,
    )
    
def create_access_token(user_id: int) -> str:
    """Membuat JWT access token."""
    
    now = datetime.now(timezone.utc)
    
    expire = now + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {
        "sub": str(user_id),
        "type": "access",
        "iat": now,
        "exp": expire,
    }
    
    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    
def create_refresh_token() -> str:
    """Membuat token acak untuk refresh session."""
    return secrets.token_urlsafe(64)

def hash_refresh_token(token: str) -> str:
    """Mengubah refresh token menjadi SHA-256 hash."""
    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()
    
def get_refresh_token_expiry() -> datetime:
    """Mendapatkan waktu kedaluwarsa refresh token dalam UTC."""
    
    expiry = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    
    return expiry.replace(tzinfo=None)