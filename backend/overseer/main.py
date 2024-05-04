from contextlib import asynccontextmanager

from fastapi import FastAPI

from overseer.db.setup import setup_db
from overseer.db.users import User


@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def home() -> list[User]:
    users = await User.all().to_list()
    return users
