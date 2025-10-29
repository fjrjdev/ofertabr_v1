
import logging
import secrets
from uuid import UUID

from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.redis import cache_service
from app.repositories.subscribers import SubscriberRepository
from app.schemas import SubscriberCreate
from app.services.email_service import EmailService
from app.services.webhook_service import webhook_service

logger = logging.getLogger(__name__)

VERIFICATION_TOKEN_TTL = 86400


class SubscriberService:
    def __init__(self, db: AsyncSession):
        self.repo = SubscriberRepository(db)
        self.email_service = EmailService()

    async def subscribe(self, subscriber_data: SubscriberCreate):
        """
        Initiate subscription process by sending verification email.
        Subscriber data is stored in Redis temporarily until verified.
        
        If subscriber previously unsubscribed, they will be reactivated.
        """
        existing_subscriber = await self.repo.get_by_email(subscriber_data.email)
        
        if existing_subscriber:
            if not existing_subscriber.is_active:
                logger.info(f"Reactivating previously unsubscribed user: {subscriber_data.email}")
                
                reactivated_subscriber = await self.repo.update(
                    existing_subscriber.id,
                    {
                        "is_active": True,
                        "unsubscribed_at": None,
                        "name": subscriber_data.name
                    }
                )
                
                if reactivated_subscriber:
                    await cache_service.clear_pattern("subscribers:*")
                    logger.info(f"Subscriber reactivated: {subscriber_data.email}")
                    
                    await webhook_service.notify_new_subscriber(
                        subscriber_id=str(reactivated_subscriber.id),
                        email=reactivated_subscriber.email,
                        name=reactivated_subscriber.name
                    )
                    
                    return {
                        "message": "Subscription reactivated successfully", 
                        "email": subscriber_data.email,
                        "reactivated": True
                    }
            else:
                logger.info(f"Subscriber already active: {subscriber_data.email}")
                return None

        verification_token = secrets.token_urlsafe(32)
        
        redis_key = f"pending_subscriber:{verification_token}"
        subscriber_dict = {
            "email": subscriber_data.email,
            "name": subscriber_data.name
        }
        
        await cache_service.set(redis_key, subscriber_dict, ttl=VERIFICATION_TOKEN_TTL)
        logger.info(f"Stored pending subscriber in Redis: {subscriber_data.email}")
        
        email_sent = await self.email_service.send_verification_email(
            to_email=subscriber_data.email,
            to_name=subscriber_data.name,
            verification_token=verification_token
        )
        
        if not email_sent:
            logger.error(f"Failed to send verification email to {subscriber_data.email}")
            await cache_service.delete(redis_key)
            return None
        
        logger.info(f"Verification email sent to {subscriber_data.email}")
        return {"message": "Verification email sent", "email": subscriber_data.email}

    async def verify_email(self, token: str):
        """
        Verify email token and create subscriber in database.
        """
        redis_key = f"pending_subscriber:{token}"
        subscriber_data = await cache_service.get(redis_key)
        
        if not subscriber_data:
            logger.warning(f"Invalid or expired verification token: {token}")
            return None
        
        if await self.repo.exists_by_email(subscriber_data["email"]):
            await cache_service.delete(redis_key)
            logger.info(f"Subscriber already exists: {subscriber_data['email']}")
            return {"already_subscribed": True}
        
        subscriber_create = SubscriberCreate(
            email=subscriber_data["email"],
            name=subscriber_data["name"]
        )
        subscriber = await self.repo.create(subscriber_create)
        
        if subscriber:
            await cache_service.delete(redis_key)
            await cache_service.clear_pattern("subscribers:*")
            logger.info(f"Subscriber verified and created: {subscriber.email}")
            
            await webhook_service.notify_new_subscriber(
                subscriber_id=str(subscriber.id),
                email=subscriber.email,
                name=subscriber.name
            )
            
        return subscriber

    async def get_all_subscribers(self):
        """Get all subscribers with caching"""
        cache_key = "subscribers:all"

        cached = await cache_service.get(cache_key)
        if cached:
            logger.info("Cache hit for all subscribers")
            from app.schemas.subscribers import SubscriberResponse
            return [SubscriberResponse(**item) for item in cached]

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
            from app.schemas.subscribers import SubscriberResponse
            return [SubscriberResponse(**item) for item in cached]

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
