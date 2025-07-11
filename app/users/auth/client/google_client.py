from dataclasses import dataclass
import httpx

from app.settings import Settings
from app.users.auth.schema import GoogleUserData


@dataclass
class GoogleClient:
    settings: Settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code) -> GoogleUserData:
        access_token: str = await self._get_user_access_token(code)
        url = f'https://www.googleapis.com/oauth2/v1/userinfo'
        async with self.async_client as client:
            user_info = await client.get(
                url,
                headers={'Authorization': f'Bearer {access_token}'}
            )
        return GoogleUserData(**user_info.json())


    async def _get_user_access_token(self, code: str) -> str:
        data = {
            'code': code,
            'client_id': self.settings.GOOGLE_CLIENT_ID,
            'client_secret': self.settings.GOOGLE_CLIENT_SECRET,
            'redirect_uri': self.settings.GOOGLE_REDIRECT_URI,
            'grant_type': 'authorization_code',
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(self.settings.GOOGLE_TOKEN_URL, data=data)
        return response.json()['access_token']


