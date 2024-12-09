from pydantic import BaseModel, Field
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    email: str = Field(min_length=3, max_length=100)
    first_name: str | None = Field(default=None, min_length=3, max_length=100)
    last_name: str | None = Field(default=None, min_length=3, max_length=100)
    age: int | None = Field(default=None, gt=0)


class UserIn(UserBase):
    password: str = Field(min_length=3, max_length=100)
    confirm_password: str = Field(min_length=3, max_length=100)


class UserOut(UserBase):
    id: int
    created_at: datetime


class Login(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    username: str


class Logout(BaseModel):
    access_token: str


class StandardResponse(BaseModel):
    success: bool
    message: str
