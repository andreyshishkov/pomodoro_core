from dataclasses import dataclass
from schemas import UserLoginSchema


@dataclass
class UserService:

    def create_user(self, username: str, password: str) -> UserLoginSchema:
        pass
