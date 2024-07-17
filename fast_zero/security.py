from datetime import datetime, timedelta
from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, encode
from jwt.exceptions import PyJWTError
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from zoneinfo import ZoneInfo

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.settings import Settings

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password_hash(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=Settings().ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({'exp': expire})

    encoded_jwt = encode(
        to_encode, Settings().SECRET_KEY, algorithm=Settings().ALGORITHM
    )

    return encoded_jwt


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    try:
        payload = decode(
            token, Settings().SECRET_KEY, algorithms=[Settings().ALGORITHM]
        )

        username: str = payload.get('sub')

        user_db = session.scalar(select(User).where(User.username == username))
        if not user_db:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail='Invalid token'
            )
    except PyJWTError:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail='Invalid token'
        )
    return user_db
