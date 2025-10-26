from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.admin import AdminLogin, Token
from app.services.admins import AdminService

router = APIRouter()


# NOTE: Registration route is disabled for security.
# Default admin credentials:
#   Email: admin@ofertabr.com
#   Username: admin
#   Password: admin123
# 
# To create additional admins, use the database directly or create a CLI tool.


@router.post(
    "/login",
    response_model=Token,
    summary="Login admin"
)
async def login(
    login_data: AdminLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    Login admin and receive JWT access token.
    
    - **email**: Admin email
    - **password**: Admin password
    
    Returns a JWT token that should be used in the Authorization header:
    `Authorization: Bearer <token>`
    """
    service = AdminService(db)
    token = await service.login(login_data)
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return token

