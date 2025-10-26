from typing import Optional
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.admins import AdminRepository
from app.schemas.admin import AdminCreate, AdminLogin, Token
from app.core.security import create_access_token
from app.core.config import settings
from app.models.admin import Admin


class AdminService:
    """Service for admin operations"""
    
    def __init__(self, db: AsyncSession):
        self.repository = AdminRepository(db)
    
    async def register_admin(self, admin_data: AdminCreate) -> Optional[Admin]:
        """
        Register a new admin.
        
        Args:
            admin_data: Admin creation data
            
        Returns:
            Created admin or None if email/username already exists
        """
        # Check if email already exists
        existing_email = await self.repository.get_by_email(admin_data.email)
        if existing_email:
            return None
        
        # Check if username already exists
        existing_username = await self.repository.get_by_username(admin_data.username)
        if existing_username:
            return None
        
        return await self.repository.create(admin_data)
    
    async def login(self, login_data: AdminLogin) -> Optional[Token]:
        """
        Authenticate admin and return access token.
        
        Args:
            login_data: Login credentials
            
        Returns:
            Token if authentication successful, None otherwise
        """
        admin = await self.repository.authenticate(login_data.email, login_data.password)
        
        if not admin:
            return None
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": admin.email},
            expires_delta=access_token_expires
        )
        
        return Token(access_token=access_token, token_type="bearer")

