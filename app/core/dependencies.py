from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_access_token
from app.services.auth_service import AuthService


security = HTTPBearer(
    scheme_name="Bearer Token",
    description="Token JWT obtido via /auth/request-code e /auth/verify-code"
)


class AuthenticatedUser:
    """
    Represents an authenticated user (admin)
    No database lookup needed - info comes from JWT
    """
    def __init__(self, email: str, user_type: str = "admin"):
        self.email = email
        self.user_type = user_type
        self.is_active = True  # All valid tokens are active
    
    def __repr__(self):
        return f"<AuthenticatedUser {self.email}>"


async def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> AuthenticatedUser:
    """
    Dependency to get current authenticated admin.
    
    Validates JWT token and extracts user info.
    No database lookup needed!
    
    Args:
        credentials: HTTP Bearer credentials from request header
        
    Returns:
        Authenticated user object
        
    Raises:
        HTTPException: If token is invalid
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    token_data = decode_access_token(token)
    
    if token_data is None or token_data.email is None:
        raise credentials_exception
    
    service = AuthService()
    is_allowed = await service._is_allowed_email(token_data.email)
    
    if not is_allowed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email no longer authorized"
        )
    
    return AuthenticatedUser(email=token_data.email)


async def get_current_active_admin(
    current_admin: AuthenticatedUser = Depends(get_current_admin)
) -> AuthenticatedUser:
    """
    Dependency to get current active admin.
    
    Args:
        current_admin: Current admin from get_current_admin dependency
        
    Returns:
        Current active admin
    """
    return current_admin

async def get_current_superuser(
    current_admin: AuthenticatedUser = Depends(get_current_admin)
) -> AuthenticatedUser:
    """
    Dependency to get current superuser admin.
    
    With passwordless auth, all authenticated users have full access.
    This is kept for API compatibility.
    
    Args:
        current_admin: Current admin from get_current_admin dependency
        
    Returns:
        Current admin (all are "superusers")
    """
    return current_admin

