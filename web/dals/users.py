from http import HTTPStatus

from fastapi import HTTPException

from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import UserToCreate
from models import User

__all__ = (
    "UserDAL",
)


class UserDAL:
    def __init__(self, session: AsyncSession):
        self.db_session = session

    async def create_user(self, user_data: UserToCreate) -> User:
        new_user = User(**user_data.dict())
        self.db_session.add(new_user)
        await self.db_session.commit()
        return new_user

    async def get_user_by_username(self, username: str) -> User:
        username = username.lower()
        query = (
            select(User)
            .where(func.lower(User.username) == username)
        )
        result = await self.db_session.execute(query)
        if not result:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="User not found"
            )
        return result.scalars().first()

    async def change_user_password(self, user_data: UserToCreate) -> None:
        username = user_data.username.lower()
        query = (
            update(User)
            .where(func.lower(User.username) == username)
            .values({"password": user_data.password})
            .returning(User.id)
        )
        result = await self.db_session.execute(query)
        if not result.fetchone():
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="User not found"
            )
