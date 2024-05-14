import uuid
from datetime import datetime
from typing import Optional

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from pymongo import IndexModel
from beanie import Document
from pydantic import BaseModel, EmailStr, Field, SecretStr


class User(Document):
    username: str = Field(min_length=4, max_length=128)
    password: SecretStr = Field(min_length=8, max_length=128)
    email: Optional[EmailStr] = None
    is_active: bool = Field(default=True)
    created_at: datetime = datetime.now()
    last_login: datetime = datetime.now()
    auth_token: uuid.UUID = uuid.uuid4()

    class Settings:
        collection = "users"
        validate_on_save = True
        indexes = [
            IndexModel("username", unique=True),
        ]

    @staticmethod
    def hash_password(password: str) -> SecretStr:
        ph = PasswordHasher()
        return SecretStr(ph.hash(password))

    def check_password(self, password: SecretStr | str) -> bool:
        ph = PasswordHasher()
        if isinstance(password, SecretStr):
            password = password.get_secret_value()
        try:
            return ph.verify(self.password.get_secret_value(), password)
        except VerifyMismatchError:
            return False

    async def set_password(self, password: str):
        self.password = self.hash_password(password)
        await self.set({"password": self.password})


class UserResponse(BaseModel):
    username: str
    email: Optional[EmailStr]
    created_at: datetime
    last_login: datetime
    auth_token: uuid.UUID


class CreateUser(BaseModel):
    username: str = Field(min_length=4, max_length=128)
    password: SecretStr = Field(min_length=8, max_length=128)
    email: Optional[EmailStr] = None


class AuthenticateUser(BaseModel):
    username: str = Field(min_length=4, max_length=128)
    password: SecretStr = Field(min_length=8, max_length=128)
