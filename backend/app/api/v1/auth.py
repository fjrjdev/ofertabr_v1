from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.config import settings
from app.core.dependencies import AuthenticatedUser, get_current_active_admin
from app.core.security import create_access_token
from app.schemas.auth import (
    AuthMagicLink,
    AuthRequest,
    AuthToken,
    AuthVerify,
    EmailManage,
    ServiceTokenRequest,
)
from app.services.auth_service import AuthService

router = APIRouter()


@router.post(
    "/request-code",
    response_model=dict,
    summary="Request access code via email"
)
async def request_access_code(data: AuthRequest):
    """
    Request a 6-digit access code sent to your email.
    
    - **email**: Your admin email address
    
    The code will be:
    - Valid for 15 minutes
    - Single use only
    - Sent to your email
    
    Example:
    ```json
    {
        "email": "admin@ofertabr.com"
    }
    ```
    """
    service = AuthService()
    success = await service.request_access_code(data.email)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not authorized or failed to send code"
        )

    return {
        "message": "Access code sent to your email",
        "email": data.email,
        "expires_in": 900
    }


@router.post(
    "/verify-code",
    response_model=AuthToken,
    summary="Verify access code and get token"
)
async def verify_access_code(data: AuthVerify):
    """
    Verify your 6-digit access code and receive JWT token.
    
    - **email**: Your admin email address
    - **code**: 6-digit code from email
    
    Returns a JWT token valid for 7 days.
    
    Use the token in Authorization header:
    `Authorization: Bearer <token>`
    
    Example:
    ```json
    {
        "email": "admin@ofertabr.com",
        "code": "123456"
    }
    ```
    """
    service = AuthService()
    token = await service.verify_access_code(data.email, data.code)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access code",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return AuthToken(
        access_token=token,
        token_type="bearer",
        expires_in=604800
    )


@router.post(
    "/request-magic-link",
    response_model=dict,
    summary="Request magic link via email"
)
async def request_magic_link(data: AuthMagicLink):
    """
    Request a magic link (one-click login) sent to your email.
    
    - **email**: Your admin email address
    
    The magic link will be:
    - Valid for 15 minutes
    - Single use only
    - Sent to your email
    - Direct access without typing code
    
    Example:
    ```json
    {
        "email": "admin@ofertabr.com"
    }
    ```
    """
    service = AuthService()
    success = await service.request_magic_link(data.email)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not authorized or failed to send magic link"
        )

    return {
        "message": "Magic link sent to your email",
        "email": data.email,
        "expires_in": 900
    }


@router.get(
    "/verify-magic",
    response_model=AuthToken,
    summary="Verify magic link token"
)
async def verify_magic_link(
    token: str = Query(..., description="Magic link token from email")
):
    """
    Verify magic link token and receive JWT token.
    
    This endpoint is called automatically when user clicks the magic link.
    
    - **token**: Magic link token (from URL parameter)
    
    Returns a JWT token valid for 7 days.
    """
    service = AuthService()
    jwt_token = await service.verify_magic_token(token)

    if not jwt_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired magic link",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return AuthToken(
        access_token=jwt_token,
        token_type="bearer",
        expires_in=604800
    )


@router.post(
    "/service-token",
    response_model=AuthToken,
    summary="Get token for service authentication (n8n, automations)"
)
async def get_service_token(data: ServiceTokenRequest):
    """
    Get JWT token for service/machine authentication (e.g., n8n workflows).
    
    This endpoint allows automated services to authenticate without email verification.
    
    **How it works:**
    1. Configure `N8N_SERVICE_SECRET` in your backend `.env` file
    2. n8n calls this endpoint with the secret
    3. Receives a JWT token valid for 7 days
    4. When token expires, n8n calls this endpoint again to renew
    
    **Security:**
    - The secret is validated against `N8N_SERVICE_SECRET` env var
    - Only services with the correct secret can get tokens
    - Tokens expire in 7 days (can be renewed automatically)
    
    **Example request:**
    ```json
    {
        "service_name": "n8n",
        "secret": "your-secret-from-env"
    }
    ```
    
    **Use in n8n:**
    - Save this token in n8n credentials
    - Use in HTTP Request headers: `Authorization: Bearer <token>`
    - Set up workflow to renew token every 6 days
    """
    if data.service_name.lower() != "n8n":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid service name. Currently only 'n8n' is supported."
        )
    
    if data.secret != settings.N8N_SERVICE_SECRET:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid service secret",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = create_access_token(
        data={"sub": f"service:{data.service_name}"},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return AuthToken(
        access_token=token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post(
    "/admin/add-email",
    response_model=dict,
    summary="Add allowed admin email"
)
async def add_allowed_email(
    data: EmailManage,
    current_admin: AuthenticatedUser = Depends(get_current_active_admin)
):
    """
    Add an email to the allowed admins list.
    
    **Protected endpoint - requires authentication**
    
    Example:
    ```json
    {
        "email": "novoadmin@exemplo.com"
    }
    ```
    """
    service = AuthService()
    success = await service.add_allowed_email(data.email)

    if not success:
        return {"message": "Email already in allowed list", "email": data.email}

    return {"message": "Email added to allowed list", "email": data.email}


@router.post(
    "/admin/remove-email",
    response_model=dict,
    summary="Remove allowed admin email"
)
async def remove_allowed_email(
    data: EmailManage,
    current_admin: AuthenticatedUser = Depends(get_current_active_admin)
):
    """
    Remove an email from the allowed admins list.
    
    **Protected endpoint - requires authentication**
    
    Example:
    ```json
    {
        "email": "admin@exemplo.com"
    }
    ```
    """
    service = AuthService()
    success = await service.remove_allowed_email(data.email)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not in allowed list"
        )

    return {"message": "Email removed from allowed list", "email": data.email}


@router.get(
    "/admin/list-emails",
    response_model=dict,
    summary="List allowed admin emails"
)
async def list_allowed_emails(
    current_admin: AuthenticatedUser = Depends(get_current_active_admin)
):
    """
    List all emails allowed to access admin endpoints.
    
    **Protected endpoint - requires authentication**
    """
    service = AuthService()
    emails = await service.list_allowed_emails()

    return {
        "allowed_emails": emails,
        "count": len(emails)
    }

