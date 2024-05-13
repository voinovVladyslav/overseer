from contextlib import asynccontextmanager

from fastapi import FastAPI

from overseer.db.setup import setup_db
from overseer.db.users import User, UserResponse
from overseer.routes.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)


@app.get("/")
async def home() -> list[UserResponse]:
    users = await User.find_all().to_list()
    return [
        UserResponse.model_validate(user, from_attributes=True)
        for user in users
    ]

