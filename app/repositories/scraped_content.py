from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from uuid import UUID
from app.models.scraped_content import ScrapedContent, ScrapedImage

from app.schemas.scraped_content import (
    ScrapedContentCreate,
    ScrapedContentUpdate,
    ScrapedContentInDBBase,
    ScrapedImageCreate,
    ScrapedImageInDBBase,
)


class ScrapedContentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, skip: int = 0, limit: int = 100):
        """Get all scraped content with pagination"""
        result = await self.db.execute(
            select(ScrapedContent)
            .options(selectinload(ScrapedContent.images))
            .offset(skip)
            .limit(limit)
        )
        contents = result.scalars().all()
        return [ScrapedContentInDBBase.model_validate(content) for content in contents]

    async def get_unprocessed(self, skip: int = 0, limit: int = 100):
        """Get unprocessed scraped content"""
        result = await self.db.execute(
            select(ScrapedContent)
            .options(selectinload(ScrapedContent.images))
            .where(ScrapedContent.is_processed == False)
            .offset(skip)
            .limit(limit)
        )
        contents = result.scalars().all()
        return [ScrapedContentInDBBase.model_validate(content) for content in contents]

    async def get_by_id(self, content_id: UUID):
        """Get scraped content by ID"""
        result = await self.db.execute(
            select(ScrapedContent)
            .options(selectinload(ScrapedContent.images))
            .where(ScrapedContent.id == content_id)
        )
        content = result.scalar_one_or_none()
        if not content:
            return None
        return ScrapedContentInDBBase.model_validate(content)

    async def get_by_url(self, source_url: str):
        """Get scraped content by source URL"""
        result = await self.db.execute(
            select(ScrapedContent)
            .options(selectinload(ScrapedContent.images))
            .where(ScrapedContent.source_url == source_url)
        )
        content = result.scalar_one_or_none()
        if not content:
            return None
        return ScrapedContentInDBBase.model_validate(content)

    async def create(self, content_data: ScrapedContentCreate):
        """Create new scraped content with images"""
        # Separar dados de imagens
        images_data = content_data.images
        content_dict = content_data.model_dump(exclude={'images'})
        
        # Criar conteúdo
        content = ScrapedContent(**content_dict)
        self.db.add(content)
        await self.db.flush()  # Flush para gerar o ID
        
        # Adicionar imagens se existirem
        if images_data:
            for img_data in images_data:
                image = ScrapedImage(
                    content_id=content.id,
                    **img_data.model_dump()
                )
                self.db.add(image)
        
        await self.db.commit()
        await self.db.refresh(content)
        
        # Carregar relacionamento de imagens
        result = await self.db.execute(
            select(ScrapedContent)
            .options(selectinload(ScrapedContent.images))
            .where(ScrapedContent.id == content.id)
        )
        content = result.scalar_one()
        
        return ScrapedContentInDBBase.model_validate(content)

    async def update(self, content_id: UUID, content_data: ScrapedContentUpdate):
        """Update scraped content"""
        result = await self.db.execute(
            select(ScrapedContent).where(ScrapedContent.id == content_id)
        )
        content = result.scalar_one_or_none()
        if not content:
            return None
        
        update_data = content_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(content, key, value)
        
        await self.db.commit()
        await self.db.refresh(content)
        
        # Carregar relacionamento de imagens
        result = await self.db.execute(
            select(ScrapedContent)
            .options(selectinload(ScrapedContent.images))
            .where(ScrapedContent.id == content_id)
        )
        content = result.scalar_one()
        
        return ScrapedContentInDBBase.model_validate(content)

    async def mark_as_processed(self, content_id: UUID):
        """Mark content as processed"""
        result = await self.db.execute(
            select(ScrapedContent).where(ScrapedContent.id == content_id)
        )
        content = result.scalar_one_or_none()
        if not content:
            return None
        
        content.is_processed = True
        await self.db.commit()
        await self.db.refresh(content)
        
        return ScrapedContentInDBBase.model_validate(content)

    async def remove(self, content_id: UUID):
        """Delete scraped content (cascade delete images)"""
        result = await self.db.execute(
            select(ScrapedContent)
            .options(selectinload(ScrapedContent.images))
            .where(ScrapedContent.id == content_id)
        )
        content = result.scalar_one_or_none()
        if not content:
            return None
        
        content_response = ScrapedContentInDBBase.model_validate(content)
        await self.db.delete(content)
        await self.db.commit()
        
        return content_response

    async def add_image(self, content_id: UUID, image_data: ScrapedImageCreate):
        """Add image to existing scraped content"""
        # Verificar se o conteúdo existe
        content = await self.db.get(ScrapedContent, content_id)
        if not content:
            return None
        
        image = ScrapedImage(
            content_id=content_id,
            **image_data.model_dump()
        )
        self.db.add(image)
        await self.db.commit()
        await self.db.refresh(image)
        
        return ScrapedImageInDBBase.model_validate(image)

    async def exists_by_url(self, source_url: str):
        """Check if content with URL already exists"""
        result = await self.db.execute(
            select(ScrapedContent.id).where(ScrapedContent.source_url == source_url)
        )
        return result.scalar_one_or_none() is not None

