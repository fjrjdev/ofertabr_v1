from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from app.schemas.newsletter import (
    NewsletterEditionCreate,
    NewsletterEditionUpdate,
    NewsletterEditionInDBBase,
)
from app.services.newsletters import NewsletterService
from app.core.database import get_db

router = APIRouter(
    prefix="/newsletters",
    tags=["newsletters"]
)

@router.get("/", response_model=List[NewsletterEditionInDBBase], response_model_exclude_none=True)
async def get_all_newsletters(db: AsyncSession = Depends(get_db)):
    """Get all newsletters"""
    service = NewsletterService(db)
    return await service.get_all_newsletters()

@router.get("/{newsletter_id}", response_model=NewsletterEditionInDBBase, response_model_exclude_none=True)
async def get_newsletter_by_id(
    newsletter_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get a newsletter by ID"""
    service = NewsletterService(db)
    newsletter = await service.get_newsletter_by_id(newsletter_id)
    if not newsletter:
        raise HTTPException(status_code=404, detail="Newsletter not found")
    return newsletter

@router.post("/", response_model=NewsletterEditionInDBBase, response_model_exclude_none=True, status_code=status.HTTP_201_CREATED)
async def create_newsletter(
    newsletter_data: NewsletterEditionCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new newsletter"""
    service = NewsletterService(db)
    return await service.create_newsletter(newsletter_data)

@router.put("/{newsletter_id}", response_model=NewsletterEditionInDBBase, response_model_exclude_none=True)
async def update_newsletter(
    newsletter_id: UUID,
    newsletter_data: NewsletterEditionUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an existing newsletter"""
    service = NewsletterService(db)
    updated = await service.update_newsletter(newsletter_id, newsletter_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Newsletter not found")
    return updated

@router.delete("/{newsletter_id}", response_model=NewsletterEditionInDBBase, response_model_exclude_none=True)
async def remove_newsletter(
    newsletter_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Delete a newsletter"""
    service = NewsletterService(db)
    deleted = await service.remove_newsletter(newsletter_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Newsletter not found")
    return deleted

