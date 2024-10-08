from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': '123',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_create_user_already_username_exist(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'user0',
            'email': 'user0@test.com',
            'password': '123',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_already_email_exist(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'user0@test.com',
            'password': '123',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users_with_users(client, user, token):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(
        '/users/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_get_user(client, user, token):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_get_user_exception(client, token, user):
    response = client.get(
        f'/users/{user.id + 1}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user_exception(client, token, other_user):
    response = client.put(
        f'/users/{other_user.id}',
        json={
            'username': 'miguel',
            'email': 'miguel@teste.com',
            'password': 'newpassword',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        'detail': 'You do not have permission to update this user'
    }


def test_update_no_changes(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        json={
            'username': user.username,
            'email': user.email,
            'password': user.clean_password,
        },
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'No changes were made'}


def test_update_users(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'miguel',
            'email': 'miguel@newemail.com',
            'password': 'newpassword',
        },
        headers={'Authorization': f'Bearer {token}'},
    )
    UserPublic.model_validate(user).model_dump()

    assert response.status_code == HTTPStatus.OK


def test_delete_users_exception(client, token, other_user):
    response = client.delete(
        f'/users/{other_user.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        'detail': 'You do not have permission to delete this user'
    }


def test_delete_users(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}
