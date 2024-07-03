from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Message, UserList, UserPublic, UserSchema
from fast_zero.security import get_password_hash, verify_password_hash

app = FastAPI()


@app.post('/users/', response_model=UserPublic, status_code=HTTPStatus.CREATED)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )
    check_user(db_user, user)
    db_user = User(
        username=user.username,
        password=get_password_hash(user.password),
        email=user.email,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


def check_user(db_user, user):  # pragma: no cover
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )


@app.get('/users/', response_model=UserList)
def read_users(
    limit: int = 10, skip: int = 0, session: Session = Depends(get_session)
):
    db_users = session.scalars(select(User).limit(limit).offset(skip))
    return {'users': db_users}


@app.get('/users/{user_id}', response_model=UserPublic)
def get_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    return db_user


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    if db_user.id != user_id:
        check_user(db_user, user)  # pragma: no cover
    if (
        db_user.username == user.username
        and db_user.email == user.email
        and db_user.password == user.password
    ):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='No changes were made',
        )
    db_user.username = user.username
    db_user.email = user.email
    db_user.password = get_password_hash(user.password)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    session.delete(db_user)
    session.commit()
    return {'message': 'User deleted'}


@app.post('/token')
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    user = session.scalar(select(User).where(User.username == form_data.username))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect username or password',
        )
    if not verify_password_hash(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect username or password',
        )