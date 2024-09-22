import datetime

from typing import Annotated

from sqlalchemy import Date, Integer, String
from sqlalchemy.orm import DeclarativeBase, mapped_column

str_256 = Annotated[str, 256]
str_128 = Annotated[str, 128]
intpk = Annotated[int, mapped_column(primary_key=True)]
published_at = Annotated[
    datetime.date,
    mapped_column(default=datetime.date.today())
]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256),
        str_128: String(128),
        intpk: Integer,
        published_at: Date,
    }


from .books import *  # noqa
from .users import *  # noqa
