from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from repository import UserRepository
from schemas import UserLoginSchema, UserCreateSchema
from service.auth import AuthService
from dependency import get_auth_service
from exception import UserNotFoundException, UserNotCorrectPasswordException

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/login', response_model=UserLoginSchema)
async def login(
        body: UserCreateSchema,
        user_service: Annotated[AuthService, Depends(get_auth_service)]
):
    try:
        return user_service.login(body.username, body.password)

    except UserNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail,
        )
    except UserNotCorrectPasswordException as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail,
        )
