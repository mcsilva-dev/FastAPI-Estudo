from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from aula1.schemas import Message

app = FastAPI()


@app.get('/', response_model=Message)
def read_root():
    return {'message': 'Ola povo'}


@app.get('/olamundo', response_class=HTMLResponse)
def hello_world():
    return """
        <html>
            <head>
                <title> Nosso olá mundo!</title>
            </head>
            <body>
                <h1> Olá Mundo </h1>
            </body>
        </html>
    """
