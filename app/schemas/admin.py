from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


# Token schemas
class Token(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token data schema"""
    email: Optional[str] = None


# Admin schemas
class AdminBase(BaseModel):
    """Base admin schema"""
    email: EmailStr
    username: str
    full_name: Optional[str] = None


class AdminCreate(AdminBase):
    """Schema for creating a new admin"""
    password: str = Field(
        ..., 
        min_length=8,
        max_length=50,
        description="Password must be between 8 and 50 characters"
    )


class AdminUpdate(BaseModel):
    """Schema for updating admin"""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8, max_length=50)
    is_active: Optional[bool] = None


class AdminLogin(BaseModel):
    """Schema for admin login"""
    email: EmailStr
    password: str


class AdminResponse(AdminBase):
    """Schema for admin response"""
    id: UUID
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

