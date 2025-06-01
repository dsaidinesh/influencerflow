import redis
from app.core.config import settings

# Create Redis connection
redis_client = redis.from_url(settings.REDIS_URL)


def get_redis():
    """Dependency to get Redis client"""
    try:
        yield redis_client
    finally:
        pass  # Redis connection pool handles closing 