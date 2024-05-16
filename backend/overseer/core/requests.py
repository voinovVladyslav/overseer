from fastapi import Request as FastAPIRequest
from overseer.db.users import User


class Request(FastAPIRequest):
    user: User
