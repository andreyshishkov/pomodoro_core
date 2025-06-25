from dataclasses import dataclass
import requests

from settings import Settings
from schemas import GoogleUserData, YandexUserData


@dataclass
class YandexClient:
    settings: Settings

    def get_user_info(self, code):
        access_token = self._get_user_access_token(code)
        url = f'https://login.yandex.ru/info?format=json'
        user_info = requests.get(
            url,
            headers={'Authorization': f'OAuth {access_token}'}
        )
        return YandexUserData(**user_info.json())


    def _get_user_access_token(self, code: str) -> str:
        data = {
            'code': code,
            'client_id': self.settings.YANDEX_CLIENT_ID,
            'client_secret': self.settings.YANDEX_CLIENT_SECRET,
            'grant_type': 'authorization_code',
        }
        headers = {
            'Content-type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(
            self.settings.YANDEX_TOKEN_URL,
            data=data,
            headers=headers,
        )
        return response.json()['access_token']