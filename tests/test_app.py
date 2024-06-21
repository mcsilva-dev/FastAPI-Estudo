from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from aula1.app import app


@pytest.fixture()
def client():
    return TestClient(app)


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Ola povo'}


def test_ola_mundo_deve_retornar_html(client):
    response = client.get('/olamundo')

    assert response.status_code == HTTPStatus.OK
    assert (
        response.text
        == """
        <html>
            <head>
                <title> Nosso olá mundo!</title>
            </head>
            <body>
                <h1> Olá Mundo </h1>
            </body>
        </html>
    """
    )


def test_create_user(client):
    response = client.post(
        '/users',
        json={'username': 'teste', 'email': 'teste@teste', 'password': '123'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'alice',
                'email': 'alice@example.com',
                'id': 1,
            }
        ]
    }


def test_update_users(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'miguel',
            'email': 'miguel@teste',
            'password': '123',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'miguel',
        'email': 'miguel@teste',
        'id': 1,
    }


def test_delete_users(client):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}
