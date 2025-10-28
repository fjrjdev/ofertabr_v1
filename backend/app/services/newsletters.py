from uuid import UUID

from app.repositories.newsletters import NewsletterRepository
from app.schemas.newsletter import (
    NewsletterEditionCreate,
    NewsletterEditionUpdate,
)
from app.services.newsletter_builder import build_newsletter_content
from app.services.scraped_content import ScrapedContentService


class NewsletterService:
    def __init__(self, db):
        self.repository = NewsletterRepository(db)
        self.db = db

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

    async def generate_newsletter_from_products(
        self,
        title: str,
        intro_text: str | None = None,
        limit: int = 10,
        only_unprocessed: bool = True
    ):
        """
        Generate newsletter automatically from scraped products
        
        Args:
            title: Newsletter title
            intro_text: Optional intro text before products
            limit: Maximum number of products to include
            only_unprocessed: If True, only use unprocessed products
            
        Returns:
            Created newsletter with auto-generated content
        """
        content_service = ScrapedContentService(self.db)

        if only_unprocessed:
            products = await content_service.get_unprocessed_contents(skip=0, limit=limit)
        else:
            products = await content_service.get_all_contents(skip=0, limit=limit)

        if not products:
            return None

        html_content = build_newsletter_content(products, intro_text)

        newsletter_data = NewsletterEditionCreate(
            title=title,
            content=html_content,
            sent_at=None,
            total_sent=0,
            scraped_id=None
        )

        newsletter = await self.repository.create(newsletter_data)

        if only_unprocessed:
            for product in products:
                await content_service.mark_as_processed(product.id)

        return newsletter
