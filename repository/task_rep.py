from sqlalchemy.orm import Session
from sqlalchemy import select, delete, update
from database import get_db_session
from models import Task, Category
from schemas import TaskSchema, TaskCreateSchema


class TaskRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_task(self, task_id) -> Task | None:
        query = select(Task).where(Task.id == task_id)
        with self.db_session() as session:
            task: Task = session.execute(query).scalar_one_or_none()
        return task

    def get_tasks(self) -> list[Task]:
        with self.db_session() as session:
            tasks: list[Task] = session.execute(select(Task)).scalars().all()
        return tasks

    def create_task(self, task: TaskCreateSchema, user_id: int) -> int:
        task_db_row = Task(
            name=task.name,
            pomodoro_number=task.pomodoro_number,
            category_id=task.category_id,
            user_id=user_id,
        )
        with self.db_session() as session:
            session.add(task_db_row)
            session.commit()
            return task_db_row.id

    def delete_task(self, task_id: int) -> None:
        with self.db_session() as session:
            session.execute(delete(Task).where(Task.id == task_id))
            session.commit()

    def get_tasks_by_category_name(self, category_name: str) -> list[Task]:
        query = select(Task).join(Category, Task.category_id == Category.id)\
        .where(Category.name == category_name)
        with self.db_session() as session:
            tasks: list[Task] = session.execute(query).scalars().all()
        return tasks

    def update_task_name(self, task_id: int, name: str) -> Task:
        query = update(Task).where(Task.id == task_id).values(name=name).returning(Task.id)
        with self.db_session() as session:
            task_id: int = session.execute(query).scalar_one_or_none()
            session.commit()
            return self.get_task(task_id)


def get_tasks_repository() -> TaskRepository:
    db_session = get_db_session()
    return TaskRepository(db_session)
