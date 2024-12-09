from datetime import datetime, timezone

from sqlmodel import SQLModel, Field

from app.core.constants import UserRolesEnum
from app.core.database import engine


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str = Field(max_length=100, min_length=3, unique=True, index=True)
    password: str = Field(max_length=100, min_length=3)
    email: str = Field(max_length=100, min_length=7)
    first_name: str | None = Field(default=None, max_length=50)
    last_name: str | None = Field(default=None, max_length=50)
    age: int | None = Field(default=None, gt=0)
    is_active: bool = Field(default=False)
    created_at: datetime | None = Field(default=datetime.now(timezone.utc))
    role: str | None = Field(default=UserRolesEnum.USER)


class BlockedToken(SQLModel, table=True):
    id: int = Field(primary_key=True)
    token: str
    test: str | None = Field(default=None)


def create_tables():
    SQLModel.metadata.create_all(engine)