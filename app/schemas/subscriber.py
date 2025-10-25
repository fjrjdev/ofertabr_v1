from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional


class SubscriberCreate(BaseModel):
    email: EmailStr
    name: str


class SubscriberResponse(BaseModel):
    id: int
    email: str
    name: str
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)