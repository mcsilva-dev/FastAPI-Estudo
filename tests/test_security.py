from jwt import decode

from fast_zero.security import (
    create_access_token,
    get_password_hash,
    verify_password_hash,
)
from fast_zero.settings import Settings


def test_security():
    password = '123'
    hash_password = get_password_hash(password)
    assert verify_password_hash(password, hash_password) is True
    assert verify_password_hash('abc', hash_password) is False


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(
        token, Settings().SECRET_KEY, algorithms=[Settings().ALGORITHM]
    )

    assert decoded['test'] == data['test']
    assert decoded['exp']