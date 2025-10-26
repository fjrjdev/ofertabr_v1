"""
Schemas for passwordless authentication
"""
from pydantic import BaseModel, EmailStr, Field


class AuthRequest(BaseModel):
    """Request access code via email"""
    email: EmailStr = Field(..., description="Admin email address")


class AuthVerify(BaseModel):
    """Verify access code and get token"""
    email: EmailStr = Field(..., description="Admin email address")
    code: str = Field(..., min_length=6, max_length=6, description="6-digit access code")


class AuthToken(BaseModel):
    """Authentication token response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int = Field(..., description="Token expiration in seconds")


class AuthMagicLink(BaseModel):
    """Request magic link via email"""
    email: EmailStr = Field(..., description="Admin email address")


class EmailManage(BaseModel):
    """Manage allowed admin email"""
    email: EmailStr = Field(..., description="Admin email address to add or remove")
