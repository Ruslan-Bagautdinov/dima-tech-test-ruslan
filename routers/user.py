from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from database.crud import get_user_by_id, get_user_accounts, get_user_payments
from database.models import User
from database.postgre_db import get_session
from database.schemas import UserResponse
from security import get_current_user

router = APIRouter()


@router.get("/user/me", response_model=UserResponse, description="""
Конечная точка `/user/me` предназначена для получения информации о текущем аутентифицированном пользователе.
""")
async def get_current_user_info(current_user: User = Depends(get_current_user),
                                session: AsyncSession = Depends(get_session)):
    logger.info(f"Fetching user info for user ID: {current_user.id}")
    user = await get_user_by_id(session, current_user.id)
    if user is None:
        logger.warning(f"User not found for ID: {current_user.id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    logger.info(f"User info fetched successfully for user ID: {current_user.id}")
    return user


@router.get("/user/me/accounts", description="""
Конечная точка `/user/me/accounts` предназначена для получения списка счетов текущего аутентифицированного пользователя.
""")
async def get_my_accounts(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    logger.info(f"Fetching accounts for user ID: {current_user.id}")
    accounts = await get_user_accounts(session, current_user.id)
    logger.info(f"Accounts fetched successfully for user ID: {current_user.id}")
    return accounts


@router.get("/user/me/payments", description="""
Конечная точка `/user/me/payments` предназначена для получения списка платежей текущего аутентифицированного пользователя.
""")
async def get_my_payments(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    logger.info(f"Fetching payments for user ID: {current_user.id}")
    payments = await get_user_payments(session, current_user.id)
    logger.info(f"Payments fetched successfully for user ID: {current_user.id}")
    return payments
