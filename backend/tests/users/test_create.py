import pytest
from httpx import AsyncClient
from fastapi import status

from overseer.db.users import User
from .urls import AUTH_REGISTER_URL


pytestmark = pytest.mark.asyncio


async def test_create_user_success(client: AsyncClient):
    payload = {
        'username': 'vladyslav',
        'password': 'strongpassword',
        'email': 'test@example.com',
    }
    response = await client.post(AUTH_REGISTER_URL, json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    assert 'auth_token' in response.json()
    assert 'password' not in response.json()

    user = await User.find_one({"username": payload["username"]})
    assert user is not None
    assert user.password != payload["password"]
    assert user.check_password(payload["password"]) is True


async def test_create_user_password_too_short(client: AsyncClient):
    payload = {
        'username': 'vladyslav',
        'password': 'short',
    }
    response = await client.post(AUTH_REGISTER_URL, json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    assert 'auth_token'not in response.json()
    assert 'password' not in response.json()

    user = await User.find_one({"username": payload["username"]})
    assert user is None


async def test_create_user_no_payload(client: AsyncClient):
    payload = {}
    response = await client.post(AUTH_REGISTER_URL, json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    assert 'auth_token'not in response.json()
    assert 'password' not in response.json()

    assert await User.find_all().to_list() == []


async def test_create_user_duplicate_username(client: AsyncClient):
    user = User(
        username='vladyslav',
        password=User.hash_password('strongpassword'),
    )
    await user.insert()
    payload = {
        'username': 'vladyslav',
        'password': 'strongpassword',
    }
    response = await client.post(AUTH_REGISTER_URL, json=payload)
    assert response.status_code == status.HTTP_409_CONFLICT

    assert 'auth_token'not in response.json()
    assert 'password' not in response.json()

    users = User.all()
    assert await users.count() == 1
