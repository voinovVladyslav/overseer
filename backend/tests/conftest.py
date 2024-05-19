from contextlib import asynccontextmanager

import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from asgi_lifespan import LifespanManager
from fastapi.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware

from overseer.db.setup import setup_db
from overseer.routes.auth import router as auth_router
from overseer.routes.users import router as users_router
from overseer.core.middleware import TokenAuthenticationBackend


@pytest_asyncio.fixture
async def app():
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await setup_db(app, testing=True)
        test_db_name = app.state.db.name
        yield
        await app.state.db_client.drop_database(test_db_name)

    middleware = [
        Middleware(
            AuthenticationMiddleware, backend=TokenAuthenticationBackend()
        ),
    ]
    app = FastAPI(lifespan=lifespan, middleware=middleware)
    app.include_router(auth_router)
    app.include_router(users_router)

    async with LifespanManager(app) as manager:
        yield manager.app


@pytest_asyncio.fixture
async def client(app):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://localhost:8000",
    ) as client:
        yield client
