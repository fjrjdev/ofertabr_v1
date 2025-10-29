from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import AuthenticatedUser, get_current_active_admin
from app.schemas.subscribers import SubscriberCreate, SubscriberResponse
from app.services.subscribers import SubscriberService

router = APIRouter()


@router.post("/", status_code=status.HTTP_202_ACCEPTED, summary="Subscribe to newsletter")
async def subscribe(subscriber_data: SubscriberCreate, db: AsyncSession = Depends(get_db)):
    """
    Subscribe to newsletter (public endpoint - no auth required).
    
    This endpoint will:
    - Store subscriber data temporarily in Redis (24h TTL)
    - Send a verification email with a unique token
    - Subscriber must verify email within 24 hours to complete subscription
    - If subscriber previously unsubscribed, they will be reactivated immediately
    
    If verification is not completed within 24 hours, the user will need to subscribe again.
    """
    service = SubscriberService(db)
    result = await service.subscribe(subscriber_data)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already subscribed"
        )
    
    if result.get("reactivated"):
        return {
            "message": "Welcome back! Your subscription has been reactivated successfully.",
            "email": result["email"],
            "reactivated": True
        }
    
    return {
        "message": "Verification email sent. Please check your inbox and verify your email within 24 hours.",
        "email": result["email"]
    }

@router.get("/verify-email/{token}", response_model=SubscriberResponse, response_model_exclude_none=True, summary="Verify email and complete subscription")
async def verify_email(token: str, db: AsyncSession = Depends(get_db)):
    """
    Verify email and complete subscription (public endpoint - no auth required).
    
    This endpoint will:
    - Validate the verification token
    - Create the subscriber in the database
    - Send a welcome email
    - Clear the temporary data from Redis
    
    The token is valid for 24 hours from the time of subscription.
    """
    service = SubscriberService(db)
    subscriber = await service.verify_email(token)
    
    if not subscriber:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token. Please subscribe again."
        )
    
    if isinstance(subscriber, dict) and subscriber.get("already_subscribed"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already verified and subscribed"
        )
    
    return subscriber

@router.get("/", response_model=list[SubscriberResponse], response_model_exclude_none=True, summary="List all subscribers")
async def list_subscribers(
    db: AsyncSession = Depends(get_db),
    _: AuthenticatedUser = Depends(get_current_active_admin)
):
    """List all subscribers (protected - requires authentication)"""
    service = SubscriberService(db)
    subscribers = await service.get_all_subscribers()
    return subscribers

@router.get("/by-id/{subscriber_id}", response_model=SubscriberResponse, response_model_exclude_none=True, summary="Get a subscriber by ID")
async def get_subscriber_by_id(
    subscriber_id: UUID,
    db: AsyncSession = Depends(get_db),
    _: AuthenticatedUser = Depends(get_current_active_admin)
):
    """Get a subscriber by ID (protected - requires authentication)"""
    service = SubscriberService(db)
    subscriber = await service.get_subscriber_by_id(subscriber_id)
    if not subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    return subscriber

@router.get("/by-email/{email}", response_model=SubscriberResponse, response_model_exclude_none=True, summary="Get a subscriber by email")
async def get_subscriber_by_email(
    email: EmailStr,
    db: AsyncSession = Depends(get_db),
    _: AuthenticatedUser = Depends(get_current_active_admin)
):
    """Get a subscriber by email (protected - requires authentication)"""
    service = SubscriberService(db)
    subscriber = await service.get_subscriber_by_email(email)
    if not subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    return subscriber

@router.patch(
    "/{subscriber_id}/unsubscribe",
    response_model=SubscriberResponse,
    response_model_exclude_none=True,
    summary="Unsubscribe from newsletter by ID (soft delete)"
)
async def unsubscribe(
    subscriber_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Unsubscribe from newsletter by subscriber ID (soft delete).
    
    **Public endpoint - no auth required (for unsubscribe links in emails)**
    
    This will:
    - Set is_active to False
    - Set unsubscribed_at to current timestamp
    - Keep subscriber data in database
    """
    service = SubscriberService(db)
    subscriber = await service.unsubscribe_subscriber(subscriber_id)
    if not subscriber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscriber not found"
        )
    return subscriber


class UnsubscribeRequest(BaseModel):
    email: EmailStr


@router.post(
    "/unsubscribe",
    status_code=status.HTTP_200_OK,
    summary="Unsubscribe from newsletter by email"
)
async def unsubscribe_by_email(
    request: UnsubscribeRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Unsubscribe from newsletter by email (soft delete).
    
    **Public endpoint - no auth required (for unsubscribe page)**
    
    This will:
    - Find subscriber by email
    - Set is_active to False
    - Set unsubscribed_at to current timestamp
    """
    service = SubscriberService(db)
    subscriber = await service.get_subscriber_by_email(request.email)
    
    if not subscriber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found in our subscription list"
        )
    
    if not subscriber.is_active:
        return {
            "message": "Email already unsubscribed",
            "email": request.email
        }
    
    await service.unsubscribe_subscriber(subscriber.id)
    
    return {
        "message": "Successfully unsubscribed from newsletter",
        "email": request.email
    }


@router.delete(
    "/{subscriber_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete subscriber permanently (hard delete)"
)
async def delete_subscriber(
    subscriber_id: UUID,
    db: AsyncSession = Depends(get_db),
    _: AuthenticatedUser = Depends(get_current_active_admin)
):
    """
    Permanently delete subscriber from database (hard delete).
    
    **Protected endpoint - requires authentication**
    
    Warning: This action cannot be undone!
    Use PATCH /unsubscribe for soft delete instead.
    """
    service = SubscriberService(db)
    success = await service.remove_subscriber(subscriber_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscriber not found"
        )
    return None
