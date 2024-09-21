from sqlalchemy.orm import Mapped

from models import Base, intpk, str_256, published_at


class Book(Base):
    __tablename__ = 'books'

    id: Mapped[intpk]
    title: Mapped[str_256]
    author: Mapped[str_256]
    publish_date: Mapped[published_at]

    def __repr__(self):
        return f"Книга {self.title} автора {self.author}"
