from repository import TaskRepository, CacheTask
from schemas import TaskSchema, TaskCreateSchema

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

    def create_task(self, body: TaskCreateSchema, user_id: int) -> TaskSchema:
        task_id = self.task_repository.create_task(body, user_id)
        task = self.task_repository.get_task(task_id)
        return TaskSchema.model_validate(task)
