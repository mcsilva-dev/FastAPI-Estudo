from http import HTTPStatus

from fastapi.testclient import TestClient

from aula1.app import app


def test_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Ola povo'}


def test_ola_mundo_deve_retornar_html():
    client = TestClient(app)

    response = client.get('/olamundo')

    assert response.status_code == HTTPStatus.OK
    assert response.text == """
        <html>
            <head>
                <title> Nosso olá mundo!</title>
            </head>
            <body>
                <h1> Olá Mundo </h1>
            </body>
        </html>
    """
