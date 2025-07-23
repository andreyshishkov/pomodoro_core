import pytest
import pytest_asyncio
from app.settings import Settings
from app.users.auth.service import AuthService
from app.users.user_profile.repository import UserRepository


@pytest.fixture
def mock_auth_service(
        google_client,
        yandex_client,
        fake_user_repository,
):
    return AuthService(
        user_repository=fake_user_repository,
        settings=Settings(),
        google_client=google_client,
        yandex_client=yandex_client,
    )


@pytest_asyncio.fixture
async def auth_service(
        google_client,
        yandex_client,
        get_db_session
):
    return AuthService(
        user_repository=UserRepository(db_session=get_db_session),
        settings=Settings(),
        google_client=google_client,
        yandex_client=yandex_client,
    )
