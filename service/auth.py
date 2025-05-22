from dataclasses import dataclass
from schemas import UserLoginSchema


@dataclass
class AuthService:
    def login(self, username: str, password: str) -> UserLoginSchema:
        pass
