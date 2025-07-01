from typing import Optional

from app.infrastructure.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class UserProfile(Base):
    __tablename__ = 'user_profiles'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=True, unique=True)
    password: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[Optional[str]]
    name: Mapped[Optional[str]]
