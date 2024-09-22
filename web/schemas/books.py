import datetime
import re

from datetime import date
from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, field_validator

from common_api_model import TunedModel

__all__ = (
    "BookToCreate",
    "BookToUpdate",
    "BookToShow"
)


def check_for_pattern(value: str) -> bool:
    pattern = r"^[A-Za-z0-9_.?,* -]{3,256}$"
    if not re.match(pattern, value):
        return False
    return True


def base_validation(value: str, field_name: str) -> bool:
    if len(value) > 256:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Слишком длинное значение",
        )
    if not check_for_pattern(value):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"{field_name} или слишком короткое, или содержит недопустимые символы",
        )
    if not any(char.isalpha() for char in value):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"{field_name} должно включать буквы"
        )


class BaseBookModel(BaseModel):
    title: str
    author: str
    publish_date: Optional[date] = None

    @field_validator("author")
    def validate_author(cls, value):
        base_validation(value, field_name="Имя автора")
        return value

    @field_validator("publish_date")
    def validate_published_at(cls, value):
        if value is None:
            return datetime.date.today()
        if value > datetime.date.today():
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Если вы владелец машины времени, напишите админу, побеседуем)"
            )
        if value < datetime.datetime.strptime("1300-01-01", "%Y-%m-%d").date():
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="А книга точно настоящая?)"
            )
        return value

    @field_validator("title")
    def validate_title(cls, value):
        base_validation(value, "Название книги")
        return value


class BookToCreate(BaseBookModel):
    pass


class BookToUpdate(BaseBookModel):
    title: Optional[str] = None
    author: Optional[str] = None


class BookToShow(TunedModel):
    id: int
    title: str
    author: str
    publish_date: date
