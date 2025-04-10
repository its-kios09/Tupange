from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.schemas.user import TokenData, UserInDB
from app.models.user import User
from app.database import get_db
from app.utils.exceptions import credentials_exception

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)

async def authenticate_user(db: AsyncSession, email: str, password: str) -> Optional[User]:
    user = await User.get_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(
    db: AsyncSession = Depends(get_db), 
    token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = await User.get_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_active_patient(current_user: User = Depends(get_current_active_user)) -> User:
    if current_user.role != "patient":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have patient privileges"
        )
    return current_user
async def get_current_active_doctor(current_user: User = Depends(get_current_active_user)) -> User:
    if current_user.role != "doctor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have doctor privileges"
        )
    return current_user
async def get_current_active_admin(current_user: User = Depends(get_current_active_user)) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have admin privileges"
        )
    return current_user

async def send_password_reset_email(db: AsyncSession, email: str):
    """Generate a password reset token and send email (simulated)"""
    user = await User.get_by_email(db, email)
    if not user:
        # Don't reveal whether email exists for security
        return
    
    reset_token = create_password_reset_token(email)
    
    # Store token in Redis with 1 hour expiration
    await redis_client.setex(
        f"password_reset:{reset_token}",
        timedelta(hours=1),
        email
    )
    
    # In production, you would send an email here with the reset link
    print(f"Password reset link: http://yourapp.com/reset-password?token={reset_token}")  # For debugging
    return {"message": "Password reset email sent if account exists"}

async def reset_password(db: AsyncSession, token: str, new_password: str):
    """Verify reset token and update password"""
    email = await verify_password_reset_token(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    user = await User.get_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.hashed_password = get_password_hash(new_password)
    await db.commit()
    
    # Delete the used token
    await redis_client.delete(f"password_reset:{token}")
    
    return {"message": "Password updated successfully"}

def create_password_reset_token(email: str) -> str:
    """Create a JWT token for password reset"""
    expires = timedelta(minutes=60)
    to_encode = {"sub": email, "type": "reset"}
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

async def verify_password_reset_token(token: str) -> Optional[str]:
    """Verify password reset token and return email if valid"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "reset":
            return None
        
        email: str = payload.get("sub")
        if email is None:
            return None
        
        # Check if token exists in Redis
        stored_email = await redis_client.get(f"password_reset:{token}")
        if stored_email != email:
            return None
            
        return email
    except JWTError:
        return None