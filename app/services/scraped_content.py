from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
import logging
from app.repositories.scraped_content import ScrapedContentRepository
from app.schemas.scraped_content import (
    ScrapedContentCreate,
    ScrapedContentUpdate,
    ScrapedImageCreate,
)
from app.core.redis import cache_service

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
        
        cached = await cache_service.get(cache_key)
        if cached:
            logger.info(f"Cache hit for unprocessed contents: {cache_key}")
            return cached
        
        contents = await self.repo.get_unprocessed(skip=skip, limit=limit)
        
        if contents:
            await cache_service.set(cache_key, [c.model_dump() for c in contents], ttl=300)
        
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

