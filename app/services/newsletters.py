from app.repositories.newsletters import NewsletterRepository
from app.schemas.newsletter import (
    NewsletterEditionCreate,
    NewsletterEditionUpdate,
)
from uuid import UUID

class NewsletterService:
    def __init__(self, db):
        self.repository = NewsletterRepository(db)

    async def get_all_newsletters(self):
        return await self.repository.get_all()

    async def get_newsletter_by_id(self, newsletter_id: UUID):
        return await self.repository.get_by_id(newsletter_id)

    async def create_newsletter(self, newsletter_data: NewsletterEditionCreate):
        return await self.repository.create(newsletter_data)

    async def update_newsletter(self, newsletter_id: UUID, newsletter_data: NewsletterEditionUpdate):
        return await self.repository.update(newsletter_id, newsletter_data)

    async def remove_newsletter(self, newsletter_id: UUID):
        return await self.repository.remove(newsletter_id)
