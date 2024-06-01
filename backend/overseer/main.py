from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware

from overseer.db.setup import setup_db
from overseer.routes.auth import router as auth_router
from overseer.routes.users import router as users_router
from overseer.core.middleware.authentication import TokenAuthenticationBackend
from overseer.chronicler.config import setup_logging


setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_db(app)
    yield


middleware = [
    Middleware(AuthenticationMiddleware, backend=TokenAuthenticationBackend())
]
app = FastAPI(lifespan=lifespan, middleware=middleware)
app.include_router(auth_router)
app.include_router(users_router)
