from pymongo.errors import DuplicateKeyError
from fastapi import APIRouter, HTTPException
from fastapi import status
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from pydantic import SecretStr

from overseer.db.users import User, UserResponse, CreateUser, AuthenticateUser


router = APIRouter(prefix='/auth', tags=['auth'])


@router.post(
    '/register',
    status_code=status.HTTP_201_CREATED,
    summary='Register a new user.',
    description=(
        'Register a new user with a username, password, '
        'and optionaly with email.'
    ),
)
async def register(user_data: CreateUser) -> UserResponse:
    ph = PasswordHasher()
    user = User(
        username=user_data.username,
        password=SecretStr(ph.hash(user_data.password.get_secret_value())),
        email=user_data.email,
    )
    try:
        await user.insert()
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Username already taken.',
        )

    return UserResponse.model_validate(user, from_attributes=True)


@router.post(
    '/token',
    status_code=status.HTTP_200_OK,
    summary='Obtain authentication token.',
    description='Obtain an authentication token.',
)
async def obtain_token(user_data: AuthenticateUser) -> UserResponse:
    ph = PasswordHasher()
    user = await User.find_one({'username': user_data.username})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid credentials.',
        )
    try:
        is_password_valid = ph.verify(
            user.password.get_secret_value(),
            user_data.password.get_secret_value(),
        )
    except VerifyMismatchError:
        is_password_valid = False

    if ph.check_needs_rehash(user.password.get_secret_value()):
        user.password = SecretStr(
            ph.hash(user_data.password.get_secret_value())
        )
        await user.set({'password': user.password})

    if not is_password_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid credentials.',
        )

    return UserResponse.model_validate(user, from_attributes=True)
