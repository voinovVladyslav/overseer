from contextlib import asynccontextmanager

import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from asgi_lifespan import LifespanManager

from overseer.db.setup import setup_db
from overseer.routes.auth import router as auth_router


@pytest_asyncio.fixture
async def app():
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await setup_db(app, testing=True)
        test_db_name = app.state.db.name
        yield
        await app.state.db_client.drop_database(test_db_name)

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
