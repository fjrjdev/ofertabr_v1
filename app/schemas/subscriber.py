from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional




class SubscriberCreate(BaseModel):
    email: EmailStr
    name: str


class SubscriberResponse(BaseModel):
    id: str 
    email: str
    name: str
    is_active: bool
    subscribed_at: datetime
    unsubscribed_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)