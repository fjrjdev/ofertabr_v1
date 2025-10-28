from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class NewsletterEditionBase(BaseModel):
    title: str
    content: str
    sent_at: datetime | None = None
    total_sent: int | None = 0
    scraped_id: UUID | None = None

class NewsletterEditionCreate(NewsletterEditionBase):
    pass

class NewsletterEditionUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    sent_at: datetime | None = None
    total_sent: int | None = None
    scraped_id: UUID | None = None

class NewsletterEditionInDBBase(NewsletterEditionBase):
    id: UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
