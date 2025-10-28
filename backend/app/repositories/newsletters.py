from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.newsletter import NewsletterEdition
from app.schemas.newsletter import (
    NewsletterEditionCreate,
    NewsletterEditionInDBBase,
    NewsletterEditionUpdate,
)


class NewsletterRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        result = await self.db.execute(select(NewsletterEdition))
        newsletters = result.scalars().all()

        return [NewsletterEditionInDBBase.model_validate(nl) for nl in newsletters]

    async def get_by_id(self, newsletter_id: UUID):
        newsletter = await self.db.get(NewsletterEdition, newsletter_id)
        if not newsletter:
            return None

        return NewsletterEditionInDBBase.model_validate(newsletter)

    async def create(self, newsletter_data: NewsletterEditionCreate):
        data = newsletter_data.model_dump()
        newsletter = NewsletterEdition(**data)
        self.db.add(newsletter)
        await self.db.commit()
        await self.db.refresh(newsletter)

        return NewsletterEditionInDBBase.model_validate(newsletter)

    async def update(self, newsletter_id: UUID, newsletter_data: NewsletterEditionUpdate):
        result = await self.db.execute(select(NewsletterEdition).where(NewsletterEdition.id == newsletter_id))
        newsletter = result.scalar_one_or_none()
        if not newsletter:
            return None

        update_data = newsletter_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(newsletter, key, value)

        await self.db.commit()
        await self.db.refresh(newsletter)
        return NewsletterEditionInDBBase.model_validate(newsletter)

    async def remove(self, newsletter_id: UUID):
        result = await self.db.execute(select(NewsletterEdition).where(NewsletterEdition.id == newsletter_id))
        newsletter = result.scalar_one_or_none()
        if not newsletter:
            return False
        await self.db.delete(newsletter)
        await self.db.commit()

        return NewsletterEditionInDBBase.model_validate(newsletter)
