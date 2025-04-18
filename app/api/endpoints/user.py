# app/api/endpoints/user.py

from fastapi import APIRouter, Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import auth_backend, fastapi_users, current_user
from app.models import User
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()

router.include_router(
    # В роутер аутентификации
    # передается объект бэкенда аутентификации.
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)

users_router = fastapi_users.get_users_router(UserRead, UserUpdate)
# Из списка эндпоинтов роутера исключаем ненужную ручку.
users_router.routes = [
    rout for rout in users_router.routes if rout.name != 'users:delete_user'
]

router.include_router(
    users_router,
    prefix='/users',
    tags=['users'],
)


@router.get("/all-users/", response_model=list[UserRead], tags=["users"])
async def get_all_users(
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users
