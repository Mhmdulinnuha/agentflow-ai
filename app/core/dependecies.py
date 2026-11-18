import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

bearer_scheme = HTTPBearer(auto_error=False)

def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db), 
)-> User:
    
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing access token", 
        headers={"www-Authenticate": "Bearer"},
    )
    
    if credentials is None:
        raise unauthorized
    
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        
        if payload.get("type") != "access":
            raise unauthorized
        
        user_id = int(payload["sub"])
        
    except (jwt.InvalidTokenError, KeyError, TypeError, ValueError): 
        raise unauthorized
    
    user = db.get(User, user_id)
    
    if not user or not user.is_active:
        raise unauthorized
    return user
        
    
