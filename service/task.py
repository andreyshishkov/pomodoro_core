from repository import TaskRepository, CacheTask
from schemas.task import TaskSchema

from dataclasses import dataclass


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: CacheTask

    def get_tasks(self):
        if tasks := self.task_cache.get_tasks():
            return tasks
        tasks = self.task_repository.get_tasks()
        tasks_schema = [TaskSchema.model_validate(task) for task in tasks]
        self.task_cache.set_tasks(tasks_schema)
        return tasks_schema
