import uuid
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from .base import TimestampMixin

class NewsletterEdition(Base, TimestampMixin):
    __tablename__ = "newsletter_editions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    total_sent = Column(Integer, default=0)

    scraped_id = Column(UUID(as_uuid=True), ForeignKey("scraped_content.id"), nullable=True)
    scraped_content = relationship("ScrapedContent", backref="newsletter_editions")
