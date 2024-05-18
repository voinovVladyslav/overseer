from fastapi import APIRouter, Request
from fastapi import status

from starlette.authentication import requires

from overseer.db.users import UserResponse


router = APIRouter(prefix='/users', tags=['users'])


@router.get(
    '/profile', status_code=status.HTTP_200_OK, summary='Get user profile.'
)
@requires('authenticated')
def profile(request: Request) -> UserResponse:
    return UserResponse.model_validate(request.user, from_attributes=True)
