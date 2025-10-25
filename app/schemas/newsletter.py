from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime

class NewsletterEditionBase(BaseModel):
    title: str
    content: str
    sent_at: Optional[datetime] = None
    total_sent: Optional[int] = 0
    scraped_id: Optional[UUID] = None

class NewsletterEditionCreate(NewsletterEditionBase):
    pass

class NewsletterEditionUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    sent_at: Optional[datetime] = None
    total_sent: Optional[int] = None
    scraped_id: Optional[UUID] = None

class NewsletterEditionInDBBase(NewsletterEditionBase):
    id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
