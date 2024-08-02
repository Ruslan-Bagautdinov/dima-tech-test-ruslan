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


@router.post("/login", description="""
Конечная точка `/login` предназначена для аутентификации пользователя и выдачи токенов доступа и обновления. После успешной аутентификации пользователь получает:

- **Access Token**: Используйте его для авторизации запросов через Swagger UI. Передайте Access Token в `Authorize`.
- **Refresh Token**: Используйте его для обновления Access Token после истечения его срока действия (30 минут) через конечную точку `/refresh_token`.

Для тестирования можно использовать следующие учетные данные:
- **Администратор**: email: admin@example.com, пароль: 123
- **Пользователь**: email: user@example.com, пароль: 456
""")
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
