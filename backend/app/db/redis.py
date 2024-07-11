import redis
from ..core.config import settings

redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)


def get_redis():
    try:
        yield redis_client
    finally:
        redis_client.close()
