from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


# Schemas para ScrapedImage
class ScrapedImageBase(BaseModel):
    image_url: str
    local_path: str | None = None
    alt_text: str | None = None
    caption: str | None = None
    width: int | None = None
    height: int | None = None
    file_size: int | None = None
    mime_type: str | None = None
    display_order: int | None = 0
    is_featured: bool | None = False


class ScrapedImageCreate(ScrapedImageBase):
    pass


class ScrapedImageUpdate(BaseModel):
    image_url: str | None = None
    local_path: str | None = None
    alt_text: str | None = None
    caption: str | None = None
    width: int | None = None
    height: int | None = None
    file_size: int | None = None
    mime_type: str | None = None
    display_order: int | None = None
    is_featured: bool | None = None


class ScrapedImageInDBBase(ScrapedImageBase):
    id: UUID
    content_id: UUID
    downloaded_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


# Schemas para ScrapedContent
class ScrapedContentBase(BaseModel):
    title: str
    content: str | None = None  # Opcional - será gerado automaticamente se não fornecido
    source_url: str
    published_at: datetime | None = None
    is_processed: bool | None = False

    product_url: str | None = None
    current_price: Decimal | None = None
    original_price: Decimal | None = None
    discount_percentage: Decimal | None = None
    installments: str | None = None
    free_shipping: bool | None = False
    store_name: str | None = None
    category: str | None = None
    rating: Decimal | None = None
    reviews_count: int | None = None


class ScrapedContentCreate(ScrapedContentBase):
    images: list[ScrapedImageCreate] | None = []


class ScrapedContentUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    source_url: str | None = None
    published_at: datetime | None = None
    is_processed: bool | None = None

    # Product-specific fields
    product_url: str | None = None
    current_price: Decimal | None = None
    original_price: Decimal | None = None
    discount_percentage: Decimal | None = None
    installments: str | None = None
    free_shipping: bool | None = None
    store_name: str | None = None
    category: str | None = None
    rating: Decimal | None = None
    reviews_count: int | None = None


class ScrapedContentInDBBase(ScrapedContentBase):
    id: UUID
    scraped_at: datetime
    created_at: datetime | None = None
    updated_at: datetime | None = None
    images: list[ScrapedImageInDBBase] | None = []

    model_config = ConfigDict(from_attributes=True)



class ScrapedContentBatchCreate(BaseModel):
    """Schema for batch creation of scraped content"""
    items: list[ScrapedContentCreate]

    model_config = ConfigDict(from_attributes=True)


class BatchResultItem(BaseModel):
    """Individual result for each item in batch"""
    source_url: str
    success: bool
    content_id: UUID | None = None
    error: str | None = None


class ScrapedContentBatchResponse(BaseModel):
    """Response schema for batch creation"""
    total: int
    created: int
    skipped: int
    failed: int
    results: list[BatchResultItem]
