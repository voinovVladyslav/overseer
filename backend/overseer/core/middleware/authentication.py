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
            token = conn.headers["Authorization"].split(" ")[1]
            user = await User.find_one({"auth_token": token})
            if not user:
                return
        except IndexError:
            return
        return AuthCredentials(scopes=['authenticated']), user
