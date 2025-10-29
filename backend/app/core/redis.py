"""
Redis client configuration and cache service
"""
import json
import logging
from typing import Any

from redis import asyncio as aioredis

from app.core.config import settings

logger = logging.getLogger(__name__)


class RedisClient:
    """Redis client singleton for caching"""

    _instance: aioredis.Redis | None = None

    @classmethod
    async def get_client(cls) -> aioredis.Redis:
        """Get or create Redis client instance"""
        if cls._instance is None:
            cls._instance = await aioredis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
            logger.info(f"Redis client connected to {settings.REDIS_URL}")
        return cls._instance

    @classmethod
    async def close(cls):
        """Close Redis connection"""
        if cls._instance:
            await cls._instance.close()
            cls._instance = None
            logger.info("Redis client disconnected")


class CacheService:
    """Service for caching operations"""

    def __init__(self):
        self.redis: aioredis.Redis | None = None

    async def _get_redis(self) -> aioredis.Redis:
        """Get Redis client"""
        if self.redis is None:
            self.redis = await RedisClient.get_client()
        return self.redis

    async def get(self, key: str) -> Any | None:
        """
        Get value from cache
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None
        """
        try:
            redis = await self._get_redis()
            value = await redis.get(key)

            if value:
                return json.loads(value)
            return None

        except Exception as e:
            logger.error(f"Error getting cache key {key}: {e}")
            return None

    async def set(
        self,
        key: str,
        value: Any,
        ttl: int | None = 300
    ) -> bool:
        """
        Set value in cache
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (default: 5 minutes, None for no expiration)
            
        Returns:
            True if successful
        """
        try:
            redis = await self._get_redis()
            serialized = json.dumps(value)

            if ttl is None:
                await redis.set(key, serialized)
            else:
                await redis.setex(key, ttl, serialized)

            return True

        except Exception as e:
            logger.error(f"Error setting cache key {key}: {e}")
            return False

    async def delete(self, key: str) -> bool:
        """
        Delete key from cache
        
        Args:
            key: Cache key
            
        Returns:
            True if successful
        """
        try:
            redis = await self._get_redis()
            await redis.delete(key)
            return True

        except Exception as e:
            logger.error(f"Error deleting cache key {key}: {e}")
            return False

    async def clear_pattern(self, pattern: str) -> int:
        """
        Clear all keys matching pattern
        
        Args:
            pattern: Pattern to match (e.g., "scraped_content:*")
            
        Returns:
            Number of keys deleted
        """
        try:
            redis = await self._get_redis()
            keys = []
            async for key in redis.scan_iter(pattern):
                keys.append(key)

            if keys:
                deleted = await redis.delete(*keys)
                return deleted
            return 0

        except Exception as e:
            logger.error(f"Error clearing cache pattern {pattern}: {e}")
            return 0

    async def ping(self) -> bool:
        """
        Check if Redis is available
        
        Returns:
            True if Redis is responding
        """
        try:
            redis = await self._get_redis()
            return await redis.ping()
        except Exception as e:
            logger.error(f"Redis ping failed: {e}")
            return False


cache_service = CacheService()

