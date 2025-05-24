from fastapi import Depends
from database import get_db_session
from repository import TaskRepository, CacheTask, UserRepository
from cache import get_redis_connection
from service import TaskService, UserService
from sqlalchemy.orm import Session


def get_task_repository() -> TaskRepository:
    db_session = get_db_session()
    return TaskRepository(db_session)


def get_tasks_cache_repository() -> CacheTask:
    redis_conn = get_redis_connection()
    return CacheTask(redis_conn)


def get_task_service(
        task_repository: TaskRepository = Depends(get_task_repository),
        task_cache: CacheTask = Depends(get_tasks_cache_repository)
) -> TaskService:
    return TaskService(
        task_repository=task_repository,
        task_cache=task_cache,
    )


def get_user_repository(db_session: Session = Depends(get_db_session)) -> UserRepository:
    return UserRepository(db_session=db_session)


def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(user_repository=user_repository)
