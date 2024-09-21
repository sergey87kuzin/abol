from sqlalchemy.orm import Mapped, mapped_column

from models import Base, intpk, str_128, str_256

__all__ = ('User',)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    username: Mapped[str_128] = mapped_column(unique=True)
    password: Mapped[str_256]

    def __repr__(self):
        return f"Пользователь {self.username}"
