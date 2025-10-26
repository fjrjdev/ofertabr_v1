from typing import Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.admin import Admin
from app.schemas.admin import AdminCreate, AdminUpdate
from app.core.security import get_password_hash


class AdminRepository:
    """Repository for Admin operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_email(self, email: str) -> Optional[Admin]:
        """Get admin by email"""
        result = await self.db.execute(
            select(Admin).where(Admin.email == email)
        )
        return result.scalar_one_or_none()
    
    async def get_by_username(self, username: str) -> Optional[Admin]:
        """Get admin by username"""
        result = await self.db.execute(
            select(Admin).where(Admin.username == username)
        )
        return result.scalar_one_or_none()
    
    async def get_by_id(self, admin_id: UUID) -> Optional[Admin]:
        """Get admin by ID"""
        result = await self.db.execute(
            select(Admin).where(Admin.id == admin_id)
        )
        return result.scalar_one_or_none()
    
    async def create(self, admin_data: AdminCreate) -> Admin:
        """Create a new admin"""
        admin = Admin(
            email=admin_data.email,
            username=admin_data.username,
            full_name=admin_data.full_name,
            hashed_password=get_password_hash(admin_data.password),
            is_active=True,
            is_superuser=False
        )
        
        self.db.add(admin)
        await self.db.commit()
        await self.db.refresh(admin)
        
        return admin
    
    async def update(self, admin_id: UUID, admin_data: AdminUpdate) -> Optional[Admin]:
        """Update an existing admin"""
        admin = await self.get_by_id(admin_id)
        
        if not admin:
            return None
        
        update_data = admin_data.model_dump(exclude_unset=True)
        
        # Hash password if provided
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
        for field, value in update_data.items():
            setattr(admin, field, value)
        
        await self.db.commit()
        await self.db.refresh(admin)
        
        return admin
    
    async def authenticate(self, email: str, password: str) -> Optional[Admin]:
        """Authenticate admin"""
        from app.core.security import verify_password
        
        admin = await self.get_by_email(email)
        
        if not admin:
            return None
        
        if not verify_password(password, admin.hashed_password):
            return None
        
        if not admin.is_active:
            return None
        
        return admin

