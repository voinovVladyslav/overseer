from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from fastapi import FastAPI

from overseer.config import base as config


async def setup_db(app: FastAPI, testing: bool = False):
    client = AsyncIOMotorClient(config.MONGO_URI)
    db = client[config.DB_NAME]
    if testing:
        db = client[config.DB_NAME + "_test"]
    app.state.db_client = client
    app.state.db = db
    await init_beanie(db, document_models=config.MODELS)
