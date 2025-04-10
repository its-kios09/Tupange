from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    PATIENT = "patient"
    DOCTOR = "doctor"
    ADMIN = "admin"
    
class UserBase(BaseModel):
    email: EmailStr
    is_active: Optional[bool] = True
    role: Optional[UserRole] = UserRole.PATIENT
    
class UserCreate(UserBase):
    password: str
    
class UserUpdate(UserBase):
    email: Optional[EmailStr]
    password: Optional[str]
    is_active: Optional[bool]
    
class UserInDB(UserBase):
    id: int
    
    class Config:
        from_attributes = True  # Updated from orm_mode=True for Pydantic V2
        
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[EmailStr] = None

# Add these new schemas for password reset
class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    token: str
    new_password: str