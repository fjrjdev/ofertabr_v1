from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class SubscriberCreate(BaseModel):
    email: EmailStr
    name: str


class SubscriberResponse(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    is_active: bool
    subscribed_at: datetime
    unsubscribed_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

