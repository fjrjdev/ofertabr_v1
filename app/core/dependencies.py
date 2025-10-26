from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.admin import Admin
from app.repositories.admins import AdminRepository


# HTTP Bearer token scheme
security = HTTPBearer()


async def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> Admin:
    """
    Dependency to get current authenticated admin.
    
    Args:
        credentials: HTTP Bearer credentials from request header
        db: Database session
        
    Returns:
        Current authenticated admin
        
    Raises:
        HTTPException: If token is invalid or admin not found
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
    
    repository = AdminRepository(db)
    admin = await repository.get_by_email(token_data.email)
    
    if admin is None:
        raise credentials_exception
    
    if not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive admin account"
        )
    
    return admin


async def get_current_active_admin(
    current_admin: Admin = Depends(get_current_admin)
) -> Admin:
    """
    Dependency to get current active admin.
    
    Args:
        current_admin: Current admin from get_current_admin dependency
        
    Returns:
        Current active admin
        
    Raises:
        HTTPException: If admin is inactive
    """
    if not current_admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive admin account"
        )
    return current_admin


async def get_current_superuser(
    current_admin: Admin = Depends(get_current_admin)
) -> Admin:
    """
    Dependency to get current superuser admin.
    
    Args:
        current_admin: Current admin from get_current_admin dependency
        
    Returns:
        Current superuser admin
        
    Raises:
        HTTPException: If admin is not a superuser
    """
    if not current_admin.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Superuser access required."
        )
    return current_admin

