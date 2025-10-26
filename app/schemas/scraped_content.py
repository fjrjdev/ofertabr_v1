from pydantic import BaseModel, ConfigDict, HttpUrl
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from decimal import Decimal


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
    content: Optional[str] = None  # Opcional - será gerado automaticamente se não fornecido
    source_url: str
    published_at: Optional[datetime] = None
    is_processed: Optional[bool] = False
    
    product_url: Optional[str] = None
    current_price: Optional[Decimal] = None
    original_price: Optional[Decimal] = None
    discount_percentage: Optional[Decimal] = None
    installments: Optional[str] = None
    free_shipping: Optional[bool] = False
    store_name: Optional[str] = None
    category: Optional[str] = None
    rating: Optional[Decimal] = None
    reviews_count: Optional[int] = None


class ScrapedContentCreate(ScrapedContentBase):
    images: Optional[List[ScrapedImageCreate]] = []


class ScrapedContentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    source_url: Optional[str] = None
    published_at: Optional[datetime] = None
    is_processed: Optional[bool] = None
    
    # Product-specific fields
    product_url: Optional[str] = None
    current_price: Optional[Decimal] = None
    original_price: Optional[Decimal] = None
    discount_percentage: Optional[Decimal] = None
    installments: Optional[str] = None
    free_shipping: Optional[bool] = None
    store_name: Optional[str] = None
    category: Optional[str] = None
    rating: Optional[Decimal] = None
    reviews_count: Optional[int] = None


class ScrapedContentInDBBase(ScrapedContentBase):
    id: UUID
    scraped_at: datetime
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    images: Optional[List[ScrapedImageInDBBase]] = []

    model_config = ConfigDict(from_attributes=True)



class ScrapedContentBatchCreate(BaseModel):
    """Schema for batch creation of scraped content"""
    items: List[ScrapedContentCreate]
    
    model_config = ConfigDict(from_attributes=True)


class BatchResultItem(BaseModel):
    """Individual result for each item in batch"""
    source_url: str
    success: bool
    content_id: Optional[UUID] = None
    error: Optional[str] = None


class ScrapedContentBatchResponse(BaseModel):
    """Response schema for batch creation"""
    total: int
    created: int
    skipped: int
    failed: int
    results: List[BatchResultItem]
