from http import HTTPStatus

from fastapi import HTTPException
from pydantic import BaseModel, field_validator

from common_api_model import TunedModel
from hashing import Hasher

__all__ = (
    "UserToCreate",
    "UserToShow",
    "Token",
    "UserPassword"
)


class UserToCreate(BaseModel):
    username: str
    password: str

    @field_validator("password")
    def validate_password(cls, value):
        password_exception = HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Придумайте другой пароль"
        )
        if len(value) < 6:
            raise password_exception
        if not any(char.isdigit() for char in value):
            raise password_exception
        if not any(char.isalpha() for char in value):
            raise password_exception
        return Hasher.get_password_hash(value)


class UserToShow(TunedModel):
    id: int
    username: str


class UserPassword(BaseModel):
    password: str


class Token(BaseModel):
    access_token: str
