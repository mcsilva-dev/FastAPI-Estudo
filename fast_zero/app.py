from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Message, UserList, UserPublic, UserSchema

app = FastAPI()


@app.post('/users/', response_model=UserPublic, status_code=HTTPStatus.CREATED)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    check_user(user, session)

    db_user = User(
        username=user.username, password=user.password, email=user.email
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


def get_dbUser(user, session):
    return session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )


def check_user(user, session):
    db_user = get_dbUser(user, session)
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
    return db_user


def check_updateUser(user, session, user_id):
    db_user = get_dbUser(user, session)
    if db_user.id == user_id:
        return db_user
    else:
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
        return db_user


@app.get('/users/', response_model=UserList)
def read_users(session: Session = Depends(get_session)):
    db_users = session.scalars(select(User))
    return {'users': db_users.fetchall()}


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
    check_updateUser(user, session, user_id)
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
    db_user.password = user.password
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
