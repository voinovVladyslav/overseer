from fastapi import APIRouter, Request
from fastapi import status

from starlette.authentication import requires

from overseer.db.users import UserResponse, UpdateUser, User


router = APIRouter(prefix='/users', tags=['users'])


@router.get(
    '/profile', status_code=status.HTTP_200_OK, summary='Get user profile.'
)
@requires('authenticated')
async def profile(request: Request) -> UserResponse:
    return UserResponse.model_validate(request.user, from_attributes=True)


@router.patch(
    '/profile', status_code=status.HTTP_200_OK, summary='Update user profile.'
)
async def update_profile(request: Request, data: UpdateUser) -> UserResponse:
    user: User = request.user
    if data.password:
        data.password = User.hash_password(data.password.get_secret_value())

    user = user.model_copy(update=data.model_dump(exclude_unset=True))
    await user.save()
    return UserResponse.model_validate(user, from_attributes=True)
