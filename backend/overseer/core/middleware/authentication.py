from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware


class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print('before request')
        response = await call_next(request)
        print('after request')
        return response
