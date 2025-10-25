from pydantic import BaseModel, ConfigDict, HttpUrl
from typing import Optional, List
from uuid import UUID
from datetime import datetime


# Schemas para ScrapedImage
class ScrapedImageBase(BaseModel):
    image_url: str
    local_path: Optional[str] = None
    alt_text: Optional[str] = None
    caption: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    display_order: Optional[int] = 0
    is_featured: Optional[bool] = False


class ScrapedImageCreate(ScrapedImageBase):
    pass


class ScrapedImageUpdate(BaseModel):
    image_url: Optional[str] = None
    local_path: Optional[str] = None
    alt_text: Optional[str] = None
    caption: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    display_order: Optional[int] = None
    is_featured: Optional[bool] = None


class ScrapedImageInDBBase(ScrapedImageBase):
    id: UUID
    content_id: UUID
    downloaded_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Schemas para ScrapedContent
class ScrapedContentBase(BaseModel):
    title: str
    content: str
    source_url: str
    published_at: Optional[datetime] = None
    is_processed: Optional[bool] = False


class ScrapedContentCreate(ScrapedContentBase):
    images: Optional[List[ScrapedImageCreate]] = []


class ScrapedContentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    source_url: Optional[str] = None
    published_at: Optional[datetime] = None
    is_processed: Optional[bool] = None


class ScrapedContentInDBBase(ScrapedContentBase):
    id: UUID
    scraped_at: datetime
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    images: Optional[List[ScrapedImageInDBBase]] = []

    model_config = ConfigDict(from_attributes=True)

