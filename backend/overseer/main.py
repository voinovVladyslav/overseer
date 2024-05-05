from contextlib import asynccontextmanager

from fastapi import FastAPI

from overseer.db.setup import setup_db
from overseer.routes.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)


@app.get("/")
async def home() -> dict[str, str]:
    return {
        'message': 'API is running',
    }
