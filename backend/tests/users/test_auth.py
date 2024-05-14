import pytest
from httpx import AsyncClient
from fastapi import status

from overseer.db.users import User


pytestmark = pytest.mark.asyncio


async def test_auth_token_success(client: AsyncClient):
    user = User(
        username='vladyslav',
        password=User.hash_password('djangodjango'),
    )
    await user.insert()
    payload = {
        'username': 'vladyslav',
        'password': 'djangodjango',
    }
    response = await client.post("/auth/token", json=payload)
    assert response.status_code == status.HTTP_200_OK


async def test_auth_token_invalid_password(client: AsyncClient):
    user = User(
        username='vladyslav',
        password=User.hash_password('djangodjango'),
    )
    await user.insert()
    payload = {
        'username': 'vladyslav',
        'password': 'invalidpassword',
    }
    response = await client.post('/auth/token', json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


async def test_auth_token_invalid_username(client: AsyncClient):
    user = User(
        username='vladyslav',
        password=User.hash_password('djangodjango'),
    )
    await user.insert()
    payload = {
        'username': 'invalidusername',
        'password': 'djangodjango',
    }

    response = await client.post('/auth/token', json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
