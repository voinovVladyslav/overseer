import pytest
from httpx import AsyncClient
from fastapi import status

from overseer.db.users import User
from .urls import USER_PROFILE_URL


pytestmark = pytest.mark.asyncio


async def test_user_profile_auth_required(client: AsyncClient):
    response = await client.get(USER_PROFILE_URL)
    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_user_profile_auth_success(client: AsyncClient):
    user = User(
        username='vladyslav',
        password=User.hash_password('djangodjango'),
    )
    await user.insert()
    response = await client.get(
        USER_PROFILE_URL,
        headers={'Authorization': f'Bearer {user.auth_token}'}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['email'] is None
    assert 'password' not in data
    assert data['username'] == user.username


async def test_user_profile_auth_invalid_token(client: AsyncClient):
    user = User(
        username='vladyslav',
        password=User.hash_password('djangodjango'),
    )
    await user.insert()
    response = await client.get(
        USER_PROFILE_URL,
        headers={'Authorization': 'Bearer invalidtoken'}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_user_profile_auth_invalid_scheme(client: AsyncClient):
    user = User(
        username='vladyslav',
        password=User.hash_password('djangodjango'),
    )
    await user.insert()
    response = await client.get(
        USER_PROFILE_URL,
        headers={'Authorization': f'{user.auth_token}'}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
