from uuid import UUID

from starlette.authentication import (
    AuthenticationBackend,
    AuthCredentials,
    UnauthenticatedUser,
    BaseUser,
)

from overseer.db.users import User


class TokenAuthenticationBackend(AuthenticationBackend):
    async def authenticate(
        self, conn
    ) -> tuple[AuthCredentials, BaseUser] | None:

        if "Authorization" not in conn.headers:
            return AuthCredentials(scopes=['anonymous']), UnauthenticatedUser()
        try:
            scheme, token = conn.headers["Authorization"].split(" ")
            if scheme != "Bearer":
                return
            user = await User.find_one({"auth_token": UUID(token)})
            if not user:
                return
        except (IndexError, ValueError):
            return
        return AuthCredentials(scopes=['authenticated']), user
