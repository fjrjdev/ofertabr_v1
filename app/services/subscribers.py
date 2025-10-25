# services/subscribers.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.subscribers import SubscriberRepository
from app.schemas import SubscriberCreate
from uuid import UUID
from pydantic import EmailStr

class SubscriberService:
    def __init__(self, db: AsyncSession):
        self.repo = SubscriberRepository(db)

    async def subscribe(self, subscriber_data: SubscriberCreate):
        if await self.repo.exists_by_email(subscriber_data.email):
            return None 
        
        subscriber = await self.repo.create(subscriber_data)
        
        return subscriber

    async def get_all_subscribers(self):
        return await self.repo.get_all()
    
    async def get_subscriber_by_id(self, subscriber_id:     UUID):
        return await self.repo.get_by_id(subscriber_id)
   
    async def get_subscriber_by_email(self, email: EmailStr):
        return await self.repo.get_by_email(email)
    
    async def unsubscribe_subscriber(self, subscriber_id: UUID):
        return await self.repo.unsubscribe(subscriber_id)
    
    async def remove_subscriber(self, subscriber_id: UUID):
        return await self.repo.remove(subscriber_id)
