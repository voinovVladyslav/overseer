from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from overseer.config import base as config


async def setup_db(testing: bool = False):
    client = AsyncIOMotorClient(config.MONGO_URI)
    db = client[config.DB_NAME]
    if testing:
        db = client[config.DB_NAME + "_test"]
    await init_beanie(db, document_models=config.MODELS)
