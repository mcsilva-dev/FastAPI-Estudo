from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from aula1.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI()

database = []


@app.get('/', response_model=Message)
def read_root():
    return {'message': 'Ola povo'}


@app.post('/users', response_model=UserPublic, status_code=HTTPStatus.CREATED)
def create_user(user: UserSchema):
    user_with_id = UserDB(id=len(database) + 1, **user.model_dump())
    database.append(user_with_id)
    return user_with_id


@app.get('/users', response_model=UserList)
def read_users():
    return {'users': database}


@app.put('/users/{user_id}')
def update_user(user_id: int, user: UserSchema):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    user_with_id = UserDB(id=user_id, **user.model_dump())
    database[user_id - 1] = user_with_id
    return user_with_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int, user: UserSchema):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    del database[user_id - 1]
    return {'message': 'User deleted'}


# @app.get('/olamundo', response_class=HTMLResponse)
# def hello_world():
#     return """
#         <html>
#             <head>
#                 <title> Nosso olá mundo!</title>
#             </head>
#             <body>
#                 <h1> Olá Mundo </h1>
#             </body>
#         </html>
#     """
