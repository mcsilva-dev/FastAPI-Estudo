from fast_zero.security import get_password_hash, verify_password_hash


def test_security():
    password = '123'
    hash_password = get_password_hash(password)
    assert verify_password_hash(password, hash_password) is True
    assert verify_password_hash('abc', hash_password) is False
