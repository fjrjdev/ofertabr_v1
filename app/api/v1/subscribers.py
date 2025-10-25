from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from pydantic import EmailStr
from app.core.database import get_db
from app.models.subscriber import Subscriber
from app.repositories.subscribers import SubscriberRepository
from app.schemas.subscribers import SubscriberCreate, SubscriberResponse
from app.services.subscribers import SubscriberService

router = APIRouter()


@router.post("/", response_model=SubscriberResponse, response_model_exclude_none=True, status_code=status.HTTP_201_CREATED)
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

@router.get("/", response_model=List[SubscriberResponse], response_model_exclude_none=True)
async def list_subscribers(
    db: AsyncSession = Depends(get_db)
):
    """List all subscribers"""
    service = SubscriberService(db)
    subscribers = await service.get_all_subscribers()
    return subscribers

@router.get("/by-id/{subscriber_id}", response_model=SubscriberResponse, response_model_exclude_none=True)
async def get_subscriber_by_id(subscriber_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get a subscriber by ID"""
    service = SubscriberService(db)
    subscriber = await service.get_subscriber_by_id(subscriber_id)
    if not subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    return subscriber

@router.get("/by-email/{email}", response_model=SubscriberResponse, response_model_exclude_none=True)
async def get_subscriber_by_email(email: EmailStr, db: AsyncSession = Depends(get_db)):
    """Get a subscriber by email"""
    service = SubscriberService(db)
    subscriber = await service.get_subscriber_by_email(email)
    if not subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    return subscriber

@router.delete("/{subscriber_id}")
async def unsubscribe(
    subscriber_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Unsubscribe from newsletter using service and repository layer"""
    service = SubscriberService(db)
    success = await service.remove_subscriber(subscriber_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscriber not found"
        )
    return {"message": "Unsubscribed successfully"}