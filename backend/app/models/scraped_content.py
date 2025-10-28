import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.models.base import TimestampMixin


class ScrapedContent(Base, TimestampMixin):
    __tablename__ = "scraped_content"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=True)  # Opcional - gerado automaticamente se não fornecido
    source_url = Column(String(1000), nullable=False)
    published_at = Column(DateTime(timezone=True), nullable=True)
    scraped_at = Column(DateTime(timezone=True), server_default=func.now())
    is_processed = Column(Boolean, default=False)

    # Product-specific fields
    product_url = Column(String(1000), nullable=True)
    current_price = Column(Numeric(10, 2), nullable=True)
    original_price = Column(Numeric(10, 2), nullable=True)
    discount_percentage = Column(Numeric(5, 2), nullable=True)
    installments = Column(String(200), nullable=True)
    free_shipping = Column(Boolean, default=False)
    store_name = Column(String(100), nullable=True)
    category = Column(String(100), nullable=True)
    rating = Column(Numeric(3, 2), nullable=True)
    reviews_count = Column(Integer, nullable=True)

    images = relationship("ScrapedImage", back_populates="content", cascade="all, delete-orphan")


class ScrapedImage(Base, TimestampMixin):
    __tablename__ = "scraped_images"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_id = Column(UUID(as_uuid=True), ForeignKey("scraped_content.id"), nullable=False, index=True)

    image_url = Column(String(1000), nullable=False)
    local_path = Column(String(500), nullable=True)
    alt_text = Column(String(500), nullable=True)
    caption = Column(Text, nullable=True)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    file_size = Column(Integer, nullable=True)
    mime_type = Column(String(50), nullable=True)
    display_order = Column(Integer, default=0)
    is_featured = Column(Boolean, default=False)
    downloaded_at = Column(DateTime(timezone=True), nullable=True)

    content = relationship("ScrapedContent", back_populates="images")
