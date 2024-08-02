from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from database.crud import (get_user_by_id,
                           create_user,
                           update_user,
                           delete_user,
                           get_user_accounts,
                           get_all_users)
from database.models import User
from database.postgre_db import get_session
from database.schemas import UserCreate, UserUpdate, UserResponse
from security import get_current_user

router = APIRouter()


@router.get("/users/all", description="""
Получить список всех пользователей. Доступно только администраторам.
""")
async def get_all_users_list(current_user: User = Depends(get_current_user),
                             session: AsyncSession = Depends(get_session)):
    logger.info(f"Admin with ID: {current_user.id} attempting to fetch all users")
    if current_user.role != "admin":
        logger.warning(f"User with ID: {current_user.id} attempted to fetch all users without admin privileges")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    users = await get_all_users(session)
    logger.info(f"All users fetched successfully")
    return [{"id": user.id, "email": user.email, "full_name": user.full_name, "role": user.role} for user in users]


@router.post("/users/new", response_model=UserResponse, description="""
Создать нового пользователя. Доступно только администраторам.

- **Тело запроса**: Данные нового пользователя в формате `UserCreate`.
""")
async def create_new_user(user: UserCreate, current_user: User = Depends(get_current_user),
                          session: AsyncSession = Depends(get_session)):
    logger.info(f"Admin with ID: {current_user.id} attempting to create new user")
    if current_user.role != "admin":
        logger.warning(f"User with ID: {current_user.id} attempted to create a user without admin privileges")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    new_user = User(
        email=user.email,
        hashed_password=user.hashed_password,
        full_name=user.full_name,
        role=user.role
    )
    created_user = await create_user(session, new_user)
    logger.info(f"New user created with ID: {created_user.id}")
    return created_user


@router.get("/users/{user_id}", response_model=UserResponse, description="""
Получить информацию о пользователе по его ID. Доступно только администраторам.

- **Параметр пути**: ID пользователя.
""")
async def get_user(user_id: int, current_user: User = Depends(get_current_user),
                   session: AsyncSession = Depends(get_session)):
    logger.info(f"Admin with ID: {current_user.id} attempting to fetch user with ID: {user_id}")
    if current_user.role != "admin":
        logger.warning(f"User with ID: {current_user.id} attempted to fetch user without admin privileges")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    user = await get_user_by_id(session, user_id)
    if user is None:
        logger.warning(f"User not found for ID: {user_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    logger.info(f"User fetched successfully for ID: {user_id}")
    return user


@router.patch("/users/{user_id}", response_model=UserResponse, description="""
Обновить информацию о пользователе по его ID. Доступно только администраторам.

- **Параметр пути**: ID пользователя.
- **Тело запроса**: Данные для обновления в формате `UserUpdate`.
""")
async def update_existing_user(user_id: int, updates: UserUpdate, current_user: User = Depends(get_current_user),
                               session: AsyncSession = Depends(get_session)):
    logger.info(f"Admin with ID: {current_user.id} attempting to update user with ID: {user_id}")
    if current_user.role != "admin":
        logger.warning(f"User with ID: {current_user.id} attempted to update user without admin privileges")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    user = await get_user_by_id(session, user_id)
    if user is None:
        logger.warning(f"User not found for ID: {user_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    for field, value in updates.dict(exclude_unset=True).items():
        setattr(user, field, value)

    user_dict = {k: v for k, v in user.__dict__.items() if k != '_sa_instance_state'}

    await update_user(session, user_id, user_dict)
    logger.info(f"User updated successfully for ID: {user_id}")
    return user


@router.delete("/users/{user_id}", description="""
Удалить пользователя по его ID. Доступно только администраторам.

- **Параметр пути**: ID пользователя.
""")
async def delete_existing_user(user_id: int, current_user: User = Depends(get_current_user),
                               session: AsyncSession = Depends(get_session)):
    logger.info(f"Admin with ID: {current_user.id} attempting to delete user with ID: {user_id}")
    if current_user.role != "admin":
        logger.warning(f"User with ID: {current_user.id} attempted to delete user without admin privileges")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    await delete_user(session, user_id)
    logger.info(f"User deleted successfully for ID: {user_id}")
    return {"detail": "User deleted"}


@router.get("/users/{user_id}/accounts", description="""
Получить список счетов пользователя по его ID. Доступно только администраторам.

- **Параметр пути**: ID пользователя.
""")
async def get_user_accounts_list(user_id: int, current_user: User = Depends(get_current_user),
                                 session: AsyncSession = Depends(get_session)):
    logger.info(f"Admin with ID: {current_user.id} attempting to fetch accounts for user with ID: {user_id}")
    if current_user.role != "admin":
        logger.warning(f"User with ID: {current_user.id} attempted to fetch accounts without admin privileges")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    accounts = await get_user_accounts(session, user_id)
    logger.info(f"Accounts fetched successfully for user ID: {user_id}")
    return accounts
