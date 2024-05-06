import uuid
from datetime import datetime
from typing import Optional

from pymongo import IndexModel
from beanie import Document
from pydantic import BaseModel, EmailStr


class User(Document):
    username: str
    password: str
    email: EmailStr
    is_active: bool = True
    created_at: datetime = datetime.now()
    last_login: datetime = datetime.now()
    auth_token: uuid.UUID = uuid.uuid4()

    class Settings:
        collection = "users"
        validate_on_save = True
        indexes = [
            IndexModel("username", unique=True),
        ]


class UserResponse(BaseModel):
    username: str
    email: EmailStr
    created_at: datetime
    last_login: datetime
    auth_token: uuid.UUID


class CreateUser(BaseModel):
    username: str
    password: str
    email: Optional[EmailStr] = None


class AuthenticateUser(BaseModel):
    username: str
    password: str
