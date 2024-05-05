from pymongo.errors import DuplicateKeyError
from fastapi import APIRouter, HTTPException
from fastapi import status
from argon2 import PasswordHasher

from overseer.db.users import User, CreateUser, UserResponse


router = APIRouter(prefix='/auth', tags=['auth'])


@router.post(
    '/register',
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary='Register a new user.',
    description=(
        'Register a new user with a username, password, '
        'and optionaly with email.'
    ),
)
async def register(user_data: CreateUser) -> UserResponse:
    ph = PasswordHasher()
    email = user_data.email or ''
    user = User(
        username=user_data.username,
        password=ph.hash(user_data.password),
        email=email,
    )
    try:
        await user.insert()
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Username already taken.',
        )

    return UserResponse.model_validate(user)
