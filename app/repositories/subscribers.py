from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.subscriber import Subscriber
from app.schemas.subscribers import SubscriberCreate


class SubscriberRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        result = await self.db.execute(select(Subscriber))
        return result.scalars().all()

    async def get_by_id(self, subscriber_id: str):
        return await self.db.get(Subscriber, subscriber_id)

    async def get_by_email(self, email: str):
        result = await self.db.execute(select(Subscriber).where(Subscriber.email == email))
        return result.scalar_one_or_none()

    async def create(self, subscriber_data: SubscriberCreate):
        subscriber = Subscriber(**subscriber_data.model_dump())
        self.db.add(subscriber)
        await self.db.commit()
        await self.db.refresh(subscriber)
        return subscriber

    async def update(self, subscriber_id: str, fields: dict):
        result = await self.db.execute(select(Subscriber).where(Subscriber.id == subscriber_id))
        subscriber = result.scalar_one_or_none()
        if not subscriber:
            return None
        for key, value in fields.items():
            setattr(subscriber, key, value)
        await self.db.commit()
        await self.db.refresh(subscriber)
        return subscriber

    async def remove(self, subscriber_id: str):
        result = await self.db.execute(select(Subscriber).where(Subscriber.id == subscriber_id))
        subscriber = result.scalar_one_or_none()
        if not subscriber:
            return False
        await self.db.delete(subscriber)
        await self.db.commit()
        return True

    async def exists_by_id(self, subscriber_id: str):
        result = await self.db.execute(select(Subscriber.id).where(Subscriber.id == subscriber_id))
        return result.scalar_one_or_none() is not None

    async def exists_by_email(self, email: str):
        result = await self.db.execute(select(Subscriber.id).where(Subscriber.email == email))
        return result.scalar_one_or_none() is not None