import httpx
from fastapi import Depends, security, Security, HTTPException

from app.users.auth.client import GoogleClient, YandexClient
from app.infrastructure.database import get_db_session
from app.tasks.repository import TaskRepository, CacheTask, UserRepository
from app.infrastructure.cache import get_redis_connection
from app.tasks.service import TaskService
from app.users.user_profile.service import UserService
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.auth.service import AuthService
from app.settings import Settings
from app.exception import TokenExpiredException, TokenNotCorrectedError


def get_task_repository(
        db_session: AsyncSession = Depends(get_db_session)
) -> TaskRepository:
    return TaskRepository(db_session)


async def get_tasks_cache_repository() -> CacheTask:
    redis_conn = get_redis_connection()
    return CacheTask(redis_conn)


async def get_task_service(
        task_repository: TaskRepository = Depends(get_task_repository),
        task_cache: CacheTask = Depends(get_tasks_cache_repository)
) -> TaskService:
    return TaskService(
        task_repository=task_repository,
        task_cache=task_cache,
    )


async def get_user_repository(db_session: AsyncSession = Depends(get_db_session)) -> UserRepository:
    return UserRepository(db_session=db_session)


async def get_async_client() -> httpx.AsyncClient:
    return httpx.AsyncClient()


async def get_google_client(
        async_client:httpx.AsyncClient = Depends(get_async_client)
) -> GoogleClient:
    return GoogleClient(
        settings=Settings(),
        async_client=async_client,
    )


async def get_yandex_client(
        async_client:httpx.AsyncClient = Depends(get_async_client)
) -> YandexClient:
    return YandexClient(
        settings=Settings(),
        async_client=async_client,
    )


async def get_auth_service(
        user_repository: UserRepository = Depends(get_user_repository),
        google_client: GoogleClient = Depends(get_google_client),
        yandex_client: YandexClient = Depends(get_yandex_client)
):
    return AuthService(
        user_repository=user_repository,
        settings=Settings(),
        google_client=google_client,
        yandex_client=yandex_client,
    )


async def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository),
        auth_service: AuthService = Depends(get_auth_service),
) -> UserService:
    return UserService(user_repository=user_repository, auth_service=auth_service)


jwt_auth = security.HTTPBearer()


async def get_request_user_id(
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

