from typing import Annotated

from fastapi import APIRouter, Depends

from dependency import get_user_service
from schemas import UserLoginSchema, UserCreateSchema
from service import UserService


router = APIRouter(prefix='/user', tags=['user'])


@router.post('/', response_model=UserLoginSchema)
async def create_user(
        user: UserCreateSchema,
        user_service: Annotated[UserService, Depends(get_user_service)]
):
    return await user_service.create_user(user.username, user.password)
