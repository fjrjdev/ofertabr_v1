from fastapi import APIRouter, HTTPException, Query, status

from app.schemas.auth import AuthMagicLink, AuthRequest, AuthToken, AuthVerify, EmailManage
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
        "expires_in": 900  # 15 minutes
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
        expires_in=604800  # 7 days
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
        "expires_in": 900  # 15 minutes
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
        expires_in=604800  # 7 days
    )


# Admin management endpoints (protected)
from fastapi import Depends as FDepends

from app.core.dependencies import AuthenticatedUser, get_current_active_admin


@router.post(
    "/admin/add-email",
    response_model=dict,
    summary="Add allowed admin email"
)
async def add_allowed_email(
    data: EmailManage,
    current_admin: AuthenticatedUser = FDepends(get_current_active_admin)
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
    current_admin: AuthenticatedUser = FDepends(get_current_active_admin)
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
    current_admin: AuthenticatedUser = FDepends(get_current_active_admin)
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

