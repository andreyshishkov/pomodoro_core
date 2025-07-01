from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from app.models import Task, Category
from app.schemas import TaskCreateSchema


class TaskRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_task(self, task_id) -> Task | None:
        query = select(Task).where(Task.id == task_id)
        async with self.db_session as session:
            task: Task = (await session.execute(query)).scalar_one_or_none()
        return task

    async def get_user_task(self, user_id: int, task_id: int) -> Task | None:
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        async with self.db_session as session:
            task: Task = (await session.execute(query)).scalar_one_or_none()
        return task

    async def get_tasks(self) -> list[Task]:
        async with self.db_session as session:
            tasks: list[Task] = (await session.execute(select(Task))).scalars().all()
        return tasks

    async def create_task(self, task: TaskCreateSchema, user_id: int) -> int:
        task_db_row = Task(
            name=task.name,
            pomodoro_number=task.pomodoro_number,
            category_id=task.category_id,
            user_id=user_id,
        )
        async with self.db_session as session:
            session.add(task_db_row)
            await session.commit()
            return task_db_row.id

    async def delete_task(self, task_id: int, user_id: int) -> None:
        async with self.db_session as session:
            await session.execute(delete(Task).where(Task.id == task_id, Task.user_id == user_id))
            await session.commit()

    async def get_tasks_by_category_name(self, category_name: str) -> list[Task]:
        query = select(Task).join(Category, Task.category_id == Category.id)\
        .where(Category.name == category_name)
        async with self.db_session as session:
            tasks: list[Task] = (await session.execute(query)).scalars().all()
        return tasks

    async def update_task_name(self, task_id: int, name: str) -> Task:
        query = update(Task).where(Task.id == task_id).values(name=name).returning(Task.id)
        async with self.db_session as session:
            task_id: int = (await session.execute(query)).scalar_one_or_none()
            await session.commit()
            return await self.get_task(task_id)
