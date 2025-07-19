import pytest
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
from jose import jwt

from app.settings import Settings
from app.users.auth.service import AuthService
from app.users.user_profile.models import UserProfile
from app.users.user_profile.schema import UserLoginSchema
from tests.fixtures.auth.auth_service import auth_service

pytestmark = pytest.mark.asyncio


async def test_get_google_redirect_url__success(auth_service: AuthService, settings):
    google_redirect_url = auth_service.get_google_redirect_url()
    settings_google_redirect_url = settings.google_redirect_url
    assert google_redirect_url == settings_google_redirect_url


async def test_get_yandex_redirect_url__success(auth_service: AuthService, settings):
    yandex_redirect_url = auth_service.get_yandex_redirect_url()
    settings_yandex_redirect_url = settings.yandex_redirect_url
    assert yandex_redirect_url == settings_yandex_redirect_url


async def test_generate_access_token__success(auth_service: AuthService, settings: Settings):
    user_id = 1

    access_token = auth_service.generate_access_token(user_id=user_id)

    decode_access_token = jwt.decode(
        access_token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ENCODE_ALGORITHM],
    )
    decoded_user_id = decode_access_token.get('user_id')

    assert user_id == decoded_user_id


async def test_get_user_id_from_access_token__success(auth_service: AuthService):
    user_id = 1

    access_token = auth_service.generate_access_token(user_id=user_id)
    decoded_user_id = auth_service.get_user_id_from_access_token(access_token)

    assert user_id == decoded_user_id


async def test_google_auth__success(auth_service: AuthService):
    code = 'fake_code'

    user = await auth_service.google_auth(code=code)
    decoded_user_id = auth_service.get_user_id_from_access_token(user.access_token)

    assert user.user_id == decoded_user_id
    assert isinstance(user, UserLoginSchema)


async def test_yandex_auth__success(auth_service: AuthService):
    code = 'fake_code'

    user = await auth_service.yandex_auth(code=code)
    decoded_user_id = auth_service.get_user_id_from_access_token(user.access_token)

    assert user.user_id == decoded_user_id
    assert isinstance(user, UserLoginSchema)