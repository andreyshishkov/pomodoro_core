from fastapi import Depends, security, Security, HTTPException

from client import GoogleClient
from database import get_db_session
from repository import TaskRepository, CacheTask, UserRepository
from cache import get_redis_connection
from service import TaskService, UserService
from sqlalchemy.orm import Session

from service.auth import AuthService
from settings import Settings
from exception import TokenExpiredException, TokenNotCorrectedError


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


def get_google_client() -> GoogleClient:
    return GoogleClient(settings=Settings())


def get_auth_service(
        user_repository: UserRepository = Depends(get_user_repository),
        google_client: GoogleClient = Depends(get_google_client)
):
    return AuthService(
        user_repository=user_repository,
        settings=Settings(),
        google_client=google_client,
    )


def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository),
        auth_service: AuthService = Depends(get_auth_service),
) -> UserService:
    return UserService(user_repository=user_repository, auth_service=auth_service)


jwt_auth = security.HTTPBearer()


def get_request_user_id(
        auth_service: AuthService = Depends(get_auth_service),
        token: security.http.HTTPAuthorizationCredentials = Security(jwt_auth)
) -> int:
    try:
        user_id = auth_service.get_user_id_from_access_token(token.credentials)
    except TokenNotCorrectedError as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail,
        )
    except TokenExpiredException as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail,
        )
    return user_id

