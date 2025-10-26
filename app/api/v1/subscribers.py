from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from pydantic import EmailStr
from app.core.database import get_db
# AUTHENTICATION TEMPORARILY DISABLED
# from app.core.dependencies import get_current_active_admin
# from app.models.admin import Admin
from app.models.subscriber import Subscriber
from app.repositories.subscribers import SubscriberRepository
from app.schemas.subscribers import SubscriberCreate, SubscriberResponse
from app.services.subscribers import SubscriberService

router = APIRouter()


@router.post("/", response_model=SubscriberResponse, response_model_exclude_none=True, status_code=status.HTTP_201_CREATED, summary="Subscribe to newsletter")
async def subscribe(subscriber_data: SubscriberCreate, db: AsyncSession = Depends(get_db)):
    """Subscribe to newsletter"""
    service = SubscriberService(db)
    subscriber = await service.subscribe(subscriber_data)
    if not subscriber:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already subscribed"
        )
    return subscriber

@router.get("/", response_model=List[SubscriberResponse], response_model_exclude_none=True, summary="List all subscribers")
async def list_subscribers(
    db: AsyncSession = Depends(get_db)
    # AUTHENTICATION TEMPORARILY DISABLED
    # current_admin: Admin = Depends(get_current_active_admin)
):
    """List all subscribers"""
    service = SubscriberService(db)
    subscribers = await service.get_all_subscribers()
    return subscribers

@router.get("/by-id/{subscriber_id}", response_model=SubscriberResponse, response_model_exclude_none=True, summary="Get a subscriber by ID")
async def get_subscriber_by_id(
    subscriber_id: UUID,
    db: AsyncSession = Depends(get_db)
    # AUTHENTICATION TEMPORARILY DISABLED
    # current_admin: Admin = Depends(get_current_active_admin)
):
    """Get a subscriber by ID"""
    service = SubscriberService(db)
    subscriber = await service.get_subscriber_by_id(subscriber_id)
    if not subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    return subscriber

@router.get("/by-email/{email}", response_model=SubscriberResponse, response_model_exclude_none=True, summary="Get a subscriber by email")
async def get_subscriber_by_email(
    email: EmailStr,
    db: AsyncSession = Depends(get_db)
    # AUTHENTICATION TEMPORARILY DISABLED
    # current_admin: Admin = Depends(get_current_active_admin)
):
    """Get a subscriber by email"""
    service = SubscriberService(db)
    subscriber = await service.get_subscriber_by_email(email)
    if not subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    return subscriber

@router.patch(
    "/{subscriber_id}/unsubscribe",
    response_model=SubscriberResponse,
    response_model_exclude_none=True,
    summary="Unsubscribe from newsletter (soft delete)"
)
async def unsubscribe(
    subscriber_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Unsubscribe from newsletter (soft delete).
    
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


@router.delete(
    "/{subscriber_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete subscriber permanently (hard delete)"
)
async def delete_subscriber(
    subscriber_id: UUID,
    db: AsyncSession = Depends(get_db)
    # AUTHENTICATION TEMPORARILY DISABLED
    # current_admin: Admin = Depends(get_current_active_admin)
):
    """
    Permanently delete subscriber from database (hard delete).
    
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