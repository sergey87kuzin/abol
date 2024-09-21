from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dals import UserDAL
from models import User
from schemas import UserToCreate, UserToShow

__all__ = (
    "create_new_user",
    "get_user_by_username_for_login",
    "change_user_password",
)


async def create_new_user(body: UserToCreate, session: AsyncSession) -> UserToShow:
    async with session.begin():
        user_dal = UserDAL(session)
        if await user_dal.get_user_by_username(username=body.username):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"User with username {body.username} already exists"
            )
        user = await user_dal.create_user(body)
        return UserToShow.model_validate(user, from_attributes=True)


async def get_user_by_username_for_login(username: str, session: AsyncSession) -> User:
    async with session.begin():
        user_dal = UserDAL(session)
        return await user_dal.get_user_by_username(username)


async def change_user_password(body: UserToCreate, session: AsyncSession) -> None:
    async with session.begin():
        user_dal = UserDAL(session)
        return await user_dal.change_user_password(body)
