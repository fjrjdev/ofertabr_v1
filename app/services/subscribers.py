
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.subscribers import SubscriberRepository
from app.schemas import SubscriberCreate
from uuid import UUID
from pydantic import EmailStr
import logging
from app.core.redis import cache_service

logger = logging.getLogger(__name__)


class SubscriberService:
    def __init__(self, db: AsyncSession):
        self.repo = SubscriberRepository(db)

    async def subscribe(self, subscriber_data: SubscriberCreate):
        if await self.repo.exists_by_email(subscriber_data.email):
            return None 
        
        subscriber = await self.repo.create(subscriber_data)
        
        if subscriber:
            await cache_service.clear_pattern("subscribers:active:*")
            logger.info("Cleared active subscribers cache after subscription")
        
        return subscriber

    async def get_all_subscribers(self):
        """Get all subscribers with caching"""
        cache_key = "subscribers:all"
        
        cached = await cache_service.get(cache_key)
        if cached:
            logger.info("Cache hit for all subscribers")
            from app.schemas.subscribers import SubscriberInDB
            return [SubscriberInDB(**item) for item in cached]
        
        subscribers = await self.repo.get_all()
        
        if subscribers:
            cache_data = [{
                "id": str(s.id),
                "name": s.name,
                "email": s.email,
                "is_active": s.is_active,
                "subscribed_at": s.subscribed_at.isoformat() if s.subscribed_at else None,
                "unsubscribed_at": s.unsubscribed_at.isoformat() if s.unsubscribed_at else None,
                "created_at": s.created_at.isoformat() if hasattr(s, 'created_at') and s.created_at else None,
                "updated_at": s.updated_at.isoformat() if hasattr(s, 'updated_at') and s.updated_at else None,
            } for s in subscribers]
            await cache_service.set(cache_key, cache_data, ttl=300)
            logger.info(f"Cached {len(cache_data)} subscribers")
        
        return subscribers
    
    async def get_active_subscribers(self):
        """Get active subscribers with caching"""
        cache_key = "subscribers:active"
        
        cached = await cache_service.get(cache_key)
        if cached:
            logger.info("Cache hit for active subscribers")
            from app.schemas.subscribers import SubscriberInDB
            return [SubscriberInDB(**item) for item in cached]
        
        subscribers = await self.repo.get_active()
        
        if subscribers:
            cache_data = [{
                "id": str(s.id),
                "name": s.name,
                "email": s.email,
                "is_active": s.is_active,
                "subscribed_at": s.subscribed_at.isoformat() if s.subscribed_at else None,
                "unsubscribed_at": s.unsubscribed_at.isoformat() if s.unsubscribed_at else None,
                "created_at": s.created_at.isoformat() if hasattr(s, 'created_at') and s.created_at else None,
                "updated_at": s.updated_at.isoformat() if hasattr(s, 'updated_at') and s.updated_at else None,
            } for s in subscribers]
            await cache_service.set(cache_key, cache_data, ttl=600)
            logger.info(f"Cached {len(cache_data)} active subscribers")
        
        return subscribers
    
    async def get_subscriber_by_id(self, subscriber_id:     UUID):
        return await self.repo.get_by_id(subscriber_id)
   
    async def get_subscriber_by_email(self, email: EmailStr):
        return await self.repo.get_by_email(email)
    
    async def unsubscribe_subscriber(self, subscriber_id: UUID):
        result = await self.repo.unsubscribe(subscriber_id)
        
        if result:
            await cache_service.clear_pattern("subscribers:*")
            logger.info("Cleared subscribers cache after unsubscribe")
        
        return result
    
    async def remove_subscriber(self, subscriber_id: UUID):
        return await self.repo.remove(subscriber_id)
