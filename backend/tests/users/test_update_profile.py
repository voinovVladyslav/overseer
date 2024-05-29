import pytest
from httpx import AsyncClient
from fastapi import status

from overseer.db.users import User
from .urls import USER_PROFILE_URL


pytestmark = pytest.mark.asyncio


async def test_user_profile_auth_required(client: AsyncClient):
    response = await client.patch(
        USER_PROFILE_URL,
        json={'email': 'test@example.com'}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_update_user_profile_success(client: AsyncClient):
    user = User(
        username='testusername',
        password=User.hash_password('strongpassword'),
    )
    await user.insert()
    response = await client.patch(
        USER_PROFILE_URL,
        headers={'Authorization': f'Bearer {user.auth_token}'},
        json={'email': 'test@example.com'}
    )
    assert response.status_code == status.HTTP_200_OK
    user = await User.get(document_id=user.id)
    assert user
    assert user.email == 'test@example.com'
    assert user.check_password('strongpassword')


async def test_update_user_profile_password_success(client: AsyncClient):
    user = User(
        username='testusername',
        password=User.hash_password('strongpassword'),
    )
    await user.insert()
    response = await client.patch(
        USER_PROFILE_URL,
        headers={'Authorization': f'Bearer {user.auth_token}'},
        json={'password': 'newstrongpassword'}
    )
    assert response.status_code == status.HTTP_200_OK
    user = await User.get(document_id=user.id)
    assert user
    assert user.check_password('newstrongpassword')


async def test_update_user_profile_password_too_short(client: AsyncClient):
    user = User(
        username='testusername',
        password=User.hash_password('strongpassword'),
    )
    await user.insert()
    response = await client.patch(
        USER_PROFILE_URL,
        headers={'Authorization': f'Bearer {user.auth_token}'},
        json={'password': 'short'}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    user = await User.get(user.id)
    assert user
    assert user.check_password('strongpassword')


async def test_update_username_success(client: AsyncClient):
    user = User(
        username='test_username',
        password=User.hash_password('strongpassword'),
    )
    await user.insert()

    response = await client.patch(
        USER_PROFILE_URL,
        headers={'Authorization': f'Bearer {user.auth_token}'},
        json={'username': 'new_test_username'}
    )
    assert response.status_code == status.HTTP_200_OK
    user = await User.get(document_id=user.id)
    assert user
    assert user.username == 'new_test_username'
    assert user.check_password('strongpassword')


async def test_update_username_already_exists(client: AsyncClient):
    user1 = User(
        username='username1',
        password=User.hash_password('strongpassword'),
    )
    await user1.insert()
    user = User(
        username='username',
        password=User.hash_password('strongpassword'),
    )
    await user.insert()
    assert user.auth_token != user1.auth_token

    response = await client.patch(
        USER_PROFILE_URL,
        headers={'Authorization': f'Bearer {user.auth_token}'},
        json={'username': 'username1'}
    )
    assert response.status_code == status.HTTP_409_CONFLICT

    user = await User.get(document_id=user.id)
    assert user
    assert user.username == 'username'
    assert user.check_password('strongpassword')

    assert await User.count() == 2
