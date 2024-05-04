from datetime import datetime

from pymongo import IndexModel
from beanie import Document


class User(Document):
    username: str
    password: str
    email: str
    is_active: bool = True
    created_at: datetime = datetime.now()
    last_login: datetime = datetime.now()

    class Settings:
        collection = "users"
        indexes = [
            IndexModel("username", unique=True),
       ]
