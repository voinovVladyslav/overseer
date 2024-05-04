from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from overseer.config import base as config
from overseer.db.users import User


async def setup_db():
    client = AsyncIOMotorClient(config.MONGO_URI)
    await init_beanie(client.overseer, document_models=[User])
