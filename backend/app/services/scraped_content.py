import logging
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.redis import cache_service
from app.repositories.scraped_content import ScrapedContentRepository
from app.schemas.scraped_content import (
    ScrapedContentCreate,
    ScrapedContentUpdate,
    ScrapedImageCreate,
)

logger = logging.getLogger(__name__)


class ScrapedContentService:
    def __init__(self, db: AsyncSession):
        self.repo = ScrapedContentRepository(db)

    async def get_all_contents(self, skip: int = 0, limit: int = 100):
        """Get all scraped contents"""
        return await self.repo.get_all(skip=skip, limit=limit)

    async def get_unprocessed_contents(self, skip: int = 0, limit: int = 100):
        """Get unprocessed scraped contents with caching"""
        cache_key = f"scraped_content:unprocessed:{skip}:{limit}"

        # Try to get from cache
        cached = await cache_service.get(cache_key)
        if cached:
            logger.info(f"Cache hit for unprocessed contents: {cache_key}")
            # Convert cached dicts back to schema objects
            from app.schemas.scraped_content import ScrapedContentInDBBase
            return [ScrapedContentInDBBase(**item) for item in cached]

        # Get from database
        contents = await self.repo.get_unprocessed(skip=skip, limit=limit)

        # Cache the results
        if contents:
            # Convert SQLAlchemy models to dicts for caching
            cache_data = []
            for content in contents:
                content_dict = {
                    "id": str(content.id),
                    "title": content.title,
                    "content": content.content,
                    "source_url": content.source_url,
                    "published_at": content.published_at.isoformat() if content.published_at else None,
                    "scraped_at": content.scraped_at.isoformat() if content.scraped_at else None,
                    "is_processed": content.is_processed,
                    "product_url": content.product_url,
                    "current_price": float(content.current_price) if content.current_price else None,
                    "original_price": float(content.original_price) if content.original_price else None,
                    "discount_percentage": float(content.discount_percentage) if content.discount_percentage else None,
                    "installments": content.installments,
                    "free_shipping": content.free_shipping,
                    "store_name": content.store_name,
                    "category": content.category,
                    "rating": float(content.rating) if content.rating else None,
                    "reviews_count": content.reviews_count,
                    "created_at": content.created_at.isoformat() if hasattr(content, 'created_at') and content.created_at else None,
                    "updated_at": content.updated_at.isoformat() if hasattr(content, 'updated_at') and content.updated_at else None,
                    "images": []
                }
                cache_data.append(content_dict)

            await cache_service.set(cache_key, cache_data, ttl=300)
            logger.info(f"Cached {len(cache_data)} unprocessed contents")

        return contents

    async def get_content_by_id(self, content_id: UUID):
        """Get scraped content by ID"""
        return await self.repo.get_by_id(content_id)

    async def get_content_by_url(self, source_url: str):
        """Get scraped content by source URL"""
        return await self.repo.get_by_url(source_url)

    async def create_content(self, content_data: ScrapedContentCreate):
        """Create new scraped content (from n8n webhook)"""
        if await self.repo.exists_by_url(content_data.source_url):
            return None

        content = await self.repo.create(content_data)

        if content:
            await cache_service.clear_pattern("scraped_content:unprocessed:*")
            logger.info("Cleared unprocessed cache after creating content")

        return content

    async def update_content(self, content_id: UUID, content_data: ScrapedContentUpdate):
        """Update scraped content"""
        return await self.repo.update(content_id, content_data)

    async def mark_as_processed(self, content_id: UUID):
        """Mark content as processed"""
        result = await self.repo.mark_as_processed(content_id)

        if result:
            await cache_service.clear_pattern("scraped_content:unprocessed:*")
            logger.info("Cleared unprocessed cache after marking as processed")

        return result

    async def remove_content(self, content_id: UUID):
        """Delete scraped content"""
        return await self.repo.remove(content_id)

    async def add_image_to_content(self, content_id: UUID, image_data: ScrapedImageCreate):
        """Add image to existing content"""
        return await self.repo.add_image(content_id, image_data)

    async def create_batch(self, contents_data: list[ScrapedContentCreate]):
        """
        Create multiple scraped contents in batch.
        Returns dict with statistics and detailed results.
        """
        results = await self.repo.create_batch(contents_data)

        # Clear cache after batch creation
        await cache_service.clear_pattern("scraped_content:unprocessed:*")
        logger.info(f"Cleared unprocessed cache after batch creation of {len(results)} items")

        # Build response with statistics
        from app.schemas.scraped_content import BatchResultItem

        created = 0
        skipped = 0
        failed = 0
        result_items = []

        for success, content_or_error, source_url in results:
            if success:
                created += 1
                result_items.append(BatchResultItem(
                    source_url=source_url,
                    success=True,
                    content_id=content_or_error.id,
                    error=None
                ))
            else:
                if content_or_error == "URL already exists":
                    skipped += 1
                else:
                    failed += 1
                result_items.append(BatchResultItem(
                    source_url=source_url,
                    success=False,
                    content_id=None,
                    error=content_or_error
                ))

        return {
            "total": len(results),
            "created": created,
            "skipped": skipped,
            "failed": failed,
            "results": result_items
        }

