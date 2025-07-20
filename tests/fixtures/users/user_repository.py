import pytest
from dataclasses import dataclass

from app.users.user_profile.schema import UserCreateSchema
from tests.fixtures.users.user_model import UserProfileFactory


@dataclass
class FakeUserRepository:
    async def get_user_by_email(self, email: str):
        return None

    async def create_user(self, user_data: UserCreateSchema):
        return UserProfileFactory()


@pytest.fixture
def fake_user_repository():
    return FakeUserRepository()