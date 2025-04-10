import aioredis
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class RedisClient:
    def __init__(self):
        self.redis = None
        self.is_connected = False

    async def connect(self):
        try:
            self.redis = aioredis.from_url(
                settings.REDIS_URL,
                decode_responses=True
            )
            await self.redis.ping()
            self.is_connected = True
            logger.info("✅ Redis connected successfully")
        except Exception as e:
            logger.error(f"❌ Redis connection failed: {e}")
            self.is_connected = False

    async def disconnect(self):
        if self.redis:
            await self.redis.close()
            self.is_connected = False
            logger.info("Redis connection closed")

    async def log_operation(self, operation: str, key: str = None, value: str = None):
        if not self.is_connected:
            logger.warning("Redis not connected - operation not logged")
            return
        
        log_message = f"Redis {operation}"
        if key:
            log_message += f" - key: {key}"
        if value:
            log_message += f" - value: {value[:50]}"  # Truncate long values
        
        logger.info(log_message)
        await self.redis.set(f"log:{operation}:{key}", str(value)[:1000], ex=86400)  # Store for 24h

    async def is_healthy(self) -> bool:
        try:
            if self.redis:
                return await self.redis.ping()
            return False
        except Exception:
            return False

redis_client = RedisClient()