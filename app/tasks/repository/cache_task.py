import json
from redis import asyncio as Redis
from app.tasks.schema import TaskSchema


class CacheTask:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_tasks(self) -> list[TaskSchema]:
        async with self.redis as redis:
            task_json = await redis.lrange('tasks', 0, -1)
            return [TaskSchema.model_validate(json.loads(task)) for task in task_json]

    async def set_tasks(self, tasks: list[TaskSchema]):
        tasks_json = [task.model_dump_json() for task in tasks]
        async with self.redis as redis:
            await redis.lpush('tasks', *tasks_json)
