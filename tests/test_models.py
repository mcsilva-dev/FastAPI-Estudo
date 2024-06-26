from fast_zero.models import User


def test_create_user(session):
    with session.begin():
        user = User(
            username='miguel',
            email='miguel@teste.com',
            password='123',
        )
        session.add(user)
    session.refresh(user)
    assert user.id == 1
