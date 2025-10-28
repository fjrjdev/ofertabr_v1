from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import AuthenticatedUser, get_current_active_admin
from app.schemas.newsletter import (
    NewsletterEditionCreate,
    NewsletterEditionInDBBase,
    NewsletterEditionUpdate,
)
from app.services.email_service import EmailService
from app.services.newsletters import NewsletterService
from app.services.subscribers import SubscriberService

router = APIRouter(
    prefix="/newsletters",
    tags=["newsletters"]
)

@router.get("/", response_model=list[NewsletterEditionInDBBase], response_model_exclude_none=True, summary="List all newsletters")
async def get_all_newsletters(
    db: AsyncSession = Depends(get_db),
    _: AuthenticatedUser = Depends(get_current_active_admin)
):
    """Get all newsletters (protected - requires authentication)"""
    service = NewsletterService(db)
    return await service.get_all_newsletters()

@router.get("/{newsletter_id}", response_model=NewsletterEditionInDBBase, response_model_exclude_none=True, summary="Get a newsletter by ID")
async def get_newsletter_by_id(
    newsletter_id: UUID,
    db: AsyncSession = Depends(get_db),
    _: AuthenticatedUser = Depends(get_current_active_admin)
):
    """Get a newsletter by ID (protected - requires authentication)"""
    service = NewsletterService(db)
    newsletter = await service.get_newsletter_by_id(newsletter_id)
    if not newsletter:
        raise HTTPException(status_code=404, detail="Newsletter not found")
    return newsletter

@router.post("/", response_model=NewsletterEditionInDBBase, response_model_exclude_none=True, status_code=status.HTTP_201_CREATED, summary="Create a newsletter")
async def create_newsletter(
    newsletter_data: NewsletterEditionCreate,
    db: AsyncSession = Depends(get_db),
    _: AuthenticatedUser = Depends(get_current_active_admin)
):
    """Create a new newsletter (protected - requires authentication)"""
    service = NewsletterService(db)
    return await service.create_newsletter(newsletter_data)

@router.put("/{newsletter_id}", response_model=NewsletterEditionInDBBase, response_model_exclude_none=True)
async def update_newsletter(
    newsletter_id: UUID,
    newsletter_data: NewsletterEditionUpdate,
    db: AsyncSession = Depends(get_db),
    _: AuthenticatedUser = Depends(get_current_active_admin)
):
    """Update an existing newsletter (protected - requires authentication)"""
    service = NewsletterService(db)
    updated = await service.update_newsletter(newsletter_id, newsletter_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Newsletter not found")
    return updated

@router.delete("/{newsletter_id}", response_model=NewsletterEditionInDBBase, response_model_exclude_none=True, summary="Delete a newsletter")
async def remove_newsletter(
    newsletter_id: UUID,
    db: AsyncSession = Depends(get_db),
    _: AuthenticatedUser = Depends(get_current_active_admin)
):
    """Delete a newsletter (protected - requires authentication)"""
    service = NewsletterService(db)
    deleted = await service.remove_newsletter(newsletter_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Newsletter not found")
    return deleted


@router.post(
    "/generate",
    response_model=NewsletterEditionInDBBase,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    summary="Generate newsletter automatically from scraped products"
)
async def generate_newsletter(
    title: str = Query(..., description="Newsletter title"),
    intro_text: str | None = Query(None, description="Optional intro text before products"),
    limit: int = Query(10, ge=1, le=50, description="Max number of products to include"),
    only_unprocessed: bool = Query(True, description="Use only unprocessed products"),
    db: AsyncSession = Depends(get_db),
    _: AuthenticatedUser = Depends(get_current_active_admin)
):
    """
    Generate newsletter automatically from scraped products.
    
    **Protected endpoint - requires authentication**
    
    This endpoint:
    1. Fetches products from scraped_content (unprocessed by default)
    2. Generates HTML content automatically using newsletter_builder
    3. Creates a new newsletter with the generated content
    4. Marks products as processed (if only_unprocessed=true)
    
    - **title**: Newsletter title
    - **intro_text**: Optional intro text before product cards
    - **limit**: Maximum number of products to include (default: 10)
    - **only_unprocessed**: If true, only uses unprocessed products and marks them as processed
    
    Returns the created newsletter with auto-generated HTML content.
    """
    newsletter_service = NewsletterService(db)

    newsletter = await newsletter_service.generate_newsletter_from_products(
        title=title,
        intro_text=intro_text,
        limit=limit,
        only_unprocessed=only_unprocessed
    )

    if not newsletter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No products available to generate newsletter"
        )

    return newsletter


@router.post(
    "/{newsletter_id}/send",
    response_model=dict,
    summary="Send newsletter to subscribers"
)
async def send_newsletter(
    newsletter_id: UUID,
    test_mode: bool = Query(False, description="Send only to test email"),
    test_email: EmailStr | None = Query(None, description="Email for testing"),
    db: AsyncSession = Depends(get_db),
    _: AuthenticatedUser = Depends(get_current_active_admin)
):
    """
    Send newsletter to all active subscribers or to a test email.
    
    **Protected endpoint - requires authentication**
    
    - **test_mode**: If true, sends only to test_email (useful for preview)
    - **test_email**: Email address for testing (required if test_mode=true)
    
    Returns statistics about the send operation.
    """

    newsletter_service = NewsletterService(db)
    newsletter = await newsletter_service.get_newsletter_by_id(newsletter_id)

    if not newsletter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Newsletter not found"
        )

    email_service = EmailService()

    if test_mode:
        if not test_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="test_email is required when test_mode=true"
            )

        success = await email_service.send_test_email(
            to_email=test_email,
            newsletter_title=newsletter.title,
            newsletter_content=newsletter.content
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send test email"
            )

        return {
            "message": "Test email sent successfully",
            "test_email": test_email,
            "mode": "test"
        }

    subscriber_service = SubscriberService(db)
    all_subscribers = await subscriber_service.get_all_subscribers()

    active_subscribers = [
        {
            "email": sub.email,
            "name": sub.name,
            "id": str(sub.id)
        }
        for sub in all_subscribers
        if sub.is_active
    ]

    if not active_subscribers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No active subscribers to send to"
        )

    stats = await email_service.send_bulk_newsletters(
        newsletter_title=newsletter.title,
        newsletter_content=newsletter.content,
        subscribers=active_subscribers
    )

    newsletter.sent_at = datetime.utcnow()
    newsletter.total_sent = stats["success"]
    await db.commit()

    return {
        "message": "Newsletter sent",
        "stats": stats,
        "mode": "production"
    }

