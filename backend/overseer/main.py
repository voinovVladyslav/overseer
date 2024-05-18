from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware

from overseer.db.setup import setup_db
from overseer.db.users import User, UserResponse
from overseer.routes.auth import router as auth_router
from overseer.core.middleware import TokenAuthenticationBackend


@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_db(app)
    yield


middleware = [
    Middleware(AuthenticationMiddleware, backend=TokenAuthenticationBackend())
]
app = FastAPI(lifespan=lifespan, middleware=middleware)
app.include_router(auth_router)


@app.get("/")
async def home(request: Request) -> list[UserResponse]:
    users = await User.find_all().to_list()
    return [
        UserResponse.model_validate(user, from_attributes=True)
        for user in users
    ]
