import redis
from settings import Settings

settings = Settings()


def get_redis_connection() -> redis.Redis:
    return redis.Redis(
        host=settings.CACHE_HOST,
        port=settings.CACHE_PORT,
        db=settings.CACHE_DB,
    )


def set_pomodoro_number():
    redis_conn = get_redis_connection()
    redis_conn.set('pomodoro_number', 1)