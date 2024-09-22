from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from typing import Annotated, Union

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from database_interaction import get_db
from handlers import get_user_by_username_for_login
from models import User
from settings import ALGORITHM, SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def authenticate_user(username: str, password: str, session: AsyncSession) -> Union[User, None]:
    user = await get_user_by_username_for_login(username, session)
    if not user:
        return
    if not pwd_context.verify(password, user.password):
        return
    return user


def create_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=120)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def check_user_auth(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: AsyncSession = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user_by_username_for_login(username, session)
    if user is None:
        raise credentials_exception
