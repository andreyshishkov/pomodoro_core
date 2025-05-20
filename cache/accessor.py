import redis
from settings import Settings

settings = Settings()


def get_redis_connection() -> redis.Redis:
    return redis.Redis(
        host='localhost',
        port=6379,
        db=0,
    )


def set_pomodoro_number():
    redis_conn = get_redis_connection()
    redis_conn.set('pomodoro_number', 1)