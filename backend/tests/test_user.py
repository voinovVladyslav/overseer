from contextlib import asynccontextmanager

import pytest_asyncio
import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from asgi_lifespan import LifespanManager

from overseer.db.setup import setup_db
from overseer.db.users import User
from overseer.routes.auth import router as auth_router


@pytest_asyncio.fixture
async def app():
    @asynccontextmanager
    async def lifespan(app):
        await setup_db(testing=True)
        yield

    app = FastAPI(lifespan=lifespan)
    app.include_router(auth_router)

    async with LifespanManager(app) as manager:
        yield manager.app


@pytest_asyncio.fixture
async def client(app):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://localhost:8000",
    ) as client:
        yield client


@pytest.mark.asyncio
async def test_home(client: AsyncClient):
    await User.create()
    payload = {
        'username': 'vladyslav',
        'password': 'djangodjango',
    }
    response = await client.post("/auth/token", json=payload)
    print(response.json())
    assert response.status_code == 200
