from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from config import (ACCESS_TOKEN_EXPIRE_MINUTES,
                    REFRESH_TOKEN_EXPIRE_MINUTES)
from database.postgre_db import get_session
from database.schemas import UserLogin
from security import (create_access_token,
                      create_refresh_token,
                      authenticate_user)

router = APIRouter()


@router.post("/login")
async def login(user: UserLogin, session: AsyncSession = Depends(get_session)):
    logger.info(f"Attempting to authenticate user with email: {user.email}")
    user_data = await authenticate_user(session, user.email, user.password)
    if not user_data:
        logger.warning(f"Authentication failed for user with email: {user.email}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_data.email, "id": user_data.id, "role": user_data.role},
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": user_data.email, "id": user_data.id, "role": user_data.role},
        expires_delta=refresh_token_expires
    )
    logger.info(f"User with email: {user_data.email} authenticated successfully")
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
