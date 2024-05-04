from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI

from overseer.config import base as config


app = FastAPI()


@app.get("/")
async def home():
    client = AsyncIOMotorClient(config.MONGO_URI)
    db_names = await client.list_database_names()

    return {"db_names": db_names}
