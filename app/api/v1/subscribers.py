from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.models.subscriber import Subscriber
from app.schemas.subscriber import SubscriberCreate, SubscriberResponse

router = APIRouter()


@router.post("/", response_model=SubscriberResponse, status_code=status.HTTP_201_CREATED)
async def subscribe(
    subscriber_data: SubscriberCreate,
    db: AsyncSession = Depends(get_db)
):
    """Subscribe to newsletter"""
    result = await db.execute(
        select(Subscriber).where(Subscriber.email == subscriber_data.email)
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already subscribed"
        )
    
    subscriber = Subscriber(**subscriber_data.model_dump())
    db.add(subscriber)
    await db.commit()
    await db.refresh(subscriber)
    
    return subscriber


@router.get("/", response_model=List[SubscriberResponse])
async def list_subscribers(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all subscribers"""
    result = await db.execute(
        select(Subscriber)
        .where(Subscriber.is_active == True)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


@router.delete("/{email}")
async def unsubscribe(
    email: str,
    db: AsyncSession = Depends(get_db)
):
    """Unsubscribe from newsletter"""
    result = await db.execute(
        select(Subscriber).where(Subscriber.email == email)
    )
    subscriber = result.scalar_one_or_none()
    
    if not subscriber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscriber not found"
        )
    
    subscriber.is_active = False
    await db.commit()
    
    return {"message": "Unsubscribed successfully"}