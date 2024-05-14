import pytest
from httpx import AsyncClient

from overseer.db.users import User


@pytest.mark.asyncio
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
    assert response.status_code == 200
