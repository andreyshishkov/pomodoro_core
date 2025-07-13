import httpx
from dataclasses import dataclass
import pytest

from app.settings import Settings


@dataclass
class FakeGoogleClient:
    settings: Settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code) -> dict:
        access_token = self._get_user_access_token(code)
        return {'fake_access_token': access_token}

    async def _get_user_access_token(self, code: str) -> str:
        return f'fake_access_token {code}'


@dataclass
class FakeYandexClient:
    settings: Settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code) -> dict:
        access_token = self._get_user_access_token(code)
        return {'fake_access_token': access_token}

    async def _get_user_access_token(self, code: str) -> str:
        return f'fake_access_token {code}'


@pytest.fixture
def google_client():
    return FakeGoogleClient(settings=Settings(), async_client=httpx.AsyncClient())


@pytest.fixture
def yandex_client():
    return FakeYandexClient(settings=Settings(), async_client=httpx.AsyncClient())
