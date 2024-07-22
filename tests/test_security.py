from http import HTTPStatus

from jwt import decode

from fast_zero.security import (
    create_access_token,
    get_password_hash,
    verify_password_hash,
)
from fast_zero.settings import settings


def test_get_password_hash():
    password = '123'
    hash_password = get_password_hash(password)
    assert verify_password_hash(password, hash_password) is True
    assert verify_password_hash('abc', hash_password) is False


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(
        token, settings().SECRET_KEY, algorithms=[settings().ALGORITHM]
    )

    assert decoded['test'] == data['test']
    assert decoded['exp']


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer invalid_token'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Invalid credentials'}
