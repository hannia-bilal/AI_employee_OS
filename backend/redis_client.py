import redis
import json
from config import settings
import logging

logger = logging.getLogger(__name__)

class RedisClient:
    def __init__(self):
        self.redis = None
        self.memory_cache = {}
        
        if settings.REDIS_URL:
            try:
                self.redis = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
                # Test connection
                self.redis.ping()
                logger.info("Connected to Redis successfully.")
            except Exception as e:
                logger.warning(f"Failed to connect to Redis at {settings.REDIS_URL}. Falling back to memory cache. Error: {e}")
                self.redis = None
        else:
            logger.info("REDIS_URL not set. Using memory cache fallback.")

    def get(self, key: str):
        if self.redis:
            val = self.redis.get(key)
            return json.loads(val) if val else None
        else:
            return self.memory_cache.get(key)

    def set(self, key: str, value: dict, ex: int = 3600):
        if self.redis:
            self.redis.set(key, json.dumps(value), ex=ex)
        else:
            self.memory_cache[key] = value

    def delete(self, key: str):
        if self.redis:
            self.redis.delete(key)
        else:
            if key in self.memory_cache:
                del self.memory_cache[key]

redis_client = RedisClient()
