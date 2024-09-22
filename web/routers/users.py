from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from database_interaction import get_db
from handlers import create_new_user
from handlers.auth import authenticate_user, create_token
from handlers.users import change_user_password
from schemas import Token, UserToCreate, UserToShow
from settings import ACCESS_TOKEN_EXPIRE_MINUTES

user_router = APIRouter()


@user_router.post("/", response_model=UserToShow)
async def create_user(
        user: UserToCreate,
        session: AsyncSession = Depends(get_db)
) -> UserToShow:
    created_user = await create_new_user(user, session)
    return created_user


@user_router.post("/change_password/{username}/")
async def change_password(
        user_data: UserToCreate,
        session: Annotated[AsyncSession, Depends(get_db)]
):
    await change_user_password(user_data, session=session)


@user_router.post("/token")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: AsyncSession = Depends(get_db)
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return Token(access_token=access_token)
