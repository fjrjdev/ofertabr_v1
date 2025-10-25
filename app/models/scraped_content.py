from sqlalchemy import  Column, ForeignKey, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import TimestampMixin
from app.core.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class ScrapedContent(Base, TimestampMixin):
    __tablename__ = "scraped_content"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    source_url = Column(String(1000), nullable=False)
    published_at = Column(DateTime(timezone=True), nullable=True)
    scraped_at = Column(DateTime(timezone=True), server_default=func.now())
    is_processed = Column(Boolean, default=False)
    
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