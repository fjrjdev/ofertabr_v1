from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from app.schemas.scraped_content import (
    ScrapedContentCreate,
    ScrapedContentUpdate,
    ScrapedContentInDBBase,
    ScrapedImageCreate,
    ScrapedImageInDBBase,
    ScrapedContentBatchResponse,
)
from app.services.scraped_content import ScrapedContentService
from app.core.database import get_db
from app.core.dependencies import get_current_active_admin, AuthenticatedUser

router = APIRouter()


@router.post(
    "/batch",
    response_model=ScrapedContentBatchResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    summary="Create multiple scraped contents (batch)",
    description="Endpoint for n8n to send multiple scraped products at once"
)
async def create_scraped_content_batch(
    contents: List[ScrapedContentCreate],
    db: AsyncSession = Depends(get_db),
    _: AuthenticatedUser = Depends(get_current_active_admin)
):
    """
    Create multiple scraped contents in a single request.
    
    **Protected endpoint - requires authentication**
    
    This endpoint is optimized for bulk imports from n8n when your AI agent
    returns multiple products (up to 100) in a single extraction.
    
    **Benefits:**
    - Single HTTP request instead of multiple calls
    - Transactional: all items processed in one database transaction
    - Detailed response with statistics and per-item results
    - Automatic cache invalidation
    
    **Response includes:**
    - `total`: Total number of items received
    - `created`: Number of successfully created items
    - `skipped`: Number of items skipped (duplicate URLs)
    - `failed`: Number of items that failed to create
    - `results`: Detailed array with status of each item
    
    **Example Request Body:**
    ```json
    [
      {
        "title": "Product 1",
        "content": "Description...",
        "source_url": "https://example.com/product-1",
        "current_price": 199.90,
        "images": [...]
      },
      {
        "title": "Product 2",
        "content": "Description...",
        "source_url": "https://example.com/product-2",
        "current_price": 299.90,
        "images": [...]
      }
    ]
    ```
    """
    if not contents:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contents list cannot be empty"
        )
    
    if len(contents) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot process more than 100 items at once"
        )
    
    service = ScrapedContentService(db)
    result = await service.create_batch(contents)
    
    return result


@router.post(
    "/",
    response_model=ScrapedContentInDBBase,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    summary="Create single scraped content",
    description="Endpoint for n8n to send single scraped product"
)
async def create_scraped_content(
    content_data: ScrapedContentCreate,
    db: AsyncSession = Depends(get_db),
    _: AuthenticatedUser = Depends(get_current_active_admin)
):
    """
    Create new scraped content from n8n webhook.
    
    **Protected endpoint - requires authentication**
    
    **Note:** For multiple products, use the `/batch` endpoint instead for better performance.
    
    - **title**: Title of the scraped content
    - **content**: Main content/body
    - **source_url**: Original URL (must be unique)
    - **published_at**: Optional publication date
    - **images**: Optional list of images
    """
    service = ScrapedContentService(db)
    content = await service.create_content(content_data)
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Content with this URL already exists"
        )
    
    return content


@router.get(
    "/",
    response_model=List[ScrapedContentInDBBase],
    response_model_exclude_none=True,
    summary="List all scraped contents"
)
async def list_scraped_contents(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Max records to return"),
    db: AsyncSession = Depends(get_db),
    _: AuthenticatedUser = Depends(get_current_active_admin)
):
    """Get all scraped contents with pagination (protected - requires authentication)"""
    service = ScrapedContentService(db)
    return await service.get_all_contents(skip=skip, limit=limit)


@router.get(
    "/unprocessed",
    response_model=List[ScrapedContentInDBBase],
    response_model_exclude_none=True,
    summary="List unprocessed contents"
)
async def list_unprocessed_contents(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Max records to return"),
    db: AsyncSession = Depends(get_db),
    _: AuthenticatedUser = Depends(get_current_active_admin)
):
    """Get all unprocessed scraped contents (protected - requires authentication)"""
    service = ScrapedContentService(db)
    return await service.get_unprocessed_contents(skip=skip, limit=limit)


@router.get(
    "/{content_id}",
    response_model=ScrapedContentInDBBase,
    response_model_exclude_none=True,
    summary="Get content by ID"
)
async def get_scraped_content_by_id(
    content_id: UUID,
    db: AsyncSession = Depends(get_db),
    _: AuthenticatedUser = Depends(get_current_active_admin)
):
    """Get a specific scraped content by ID (protected - requires authentication)"""
    service = ScrapedContentService(db)
    content = await service.get_content_by_id(content_id)
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scraped content not found"
        )
    
    return content


@router.patch(
    "/{content_id}/mark-processed",
    response_model=ScrapedContentInDBBase,
    response_model_exclude_none=True,
    summary="Mark content as processed"
)
async def mark_content_as_processed(
    content_id: UUID,
    db: AsyncSession = Depends(get_db),
    _: AuthenticatedUser = Depends(get_current_active_admin)
):
    """Mark content as processed (protected - requires authentication)"""
    service = ScrapedContentService(db)
    content = await service.mark_as_processed(content_id)
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scraped content not found"
        )
    
    return content


@router.put(
    "/{content_id}",
    response_model=ScrapedContentInDBBase,
    response_model_exclude_none=True,
    summary="Update scraped content"
)
async def update_scraped_content(
    content_id: UUID,
    content_data: ScrapedContentUpdate,
    db: AsyncSession = Depends(get_db),
    _: AuthenticatedUser = Depends(get_current_active_admin)
):
    """Update an existing scraped content (protected - requires authentication)"""
    service = ScrapedContentService(db)
    updated = await service.update_content(content_id, content_data)
    
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scraped content not found"
        )
    
    return updated


@router.delete(
    "/{content_id}",
    response_model=ScrapedContentInDBBase,
    response_model_exclude_none=True,
    summary="Delete scraped content"
)
async def delete_scraped_content(
    content_id: UUID,
    db: AsyncSession = Depends(get_db),
    _: AuthenticatedUser = Depends(get_current_active_admin)
):
    """Delete a scraped content and its images (protected - requires authentication)"""
    service = ScrapedContentService(db)
    deleted = await service.remove_content(content_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scraped content not found"
        )
    
    return deleted


@router.post(
    "/{content_id}/images",
    response_model=ScrapedImageInDBBase,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    summary="Add image to content"
)
async def add_image_to_content(
    content_id: UUID,
    image_data: ScrapedImageCreate,
    db: AsyncSession = Depends(get_db),
    _: AuthenticatedUser = Depends(get_current_active_admin)
):
    """Add an image to existing scraped content (protected - requires authentication)"""
    service = ScrapedContentService(db)
    image = await service.add_image_to_content(content_id, image_data)
    
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scraped content not found"
        )
    
    return image

