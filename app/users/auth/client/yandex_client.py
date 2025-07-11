from dataclasses import dataclass
import httpx

from app.settings import Settings
from app.users.auth.schema import YandexUserData


@dataclass
class YandexClient:
    settings: Settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code):
        access_token: str = await self._get_user_access_token(code)
        url = f'https://login.yandex.ru/info?format=json'
        async with self.async_client as client:
            user_info = await client.get(
                url,
                headers={'Authorization': f'OAuth {access_token}'}
            )
        return YandexUserData(**user_info.json())


    async def _get_user_access_token(self, code: str) -> str:
        data = {
            'code': code,
            'client_id': self.settings.YANDEX_CLIENT_ID,
            'client_secret': self.settings.YANDEX_CLIENT_SECRET,
            'grant_type': 'authorization_code',
        }
        headers = {
            'Content-type': 'application/x-www-form-urlencoded'
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.settings.YANDEX_TOKEN_URL,
                data=data,
                headers=headers,
            )
        return response.json()['access_token']