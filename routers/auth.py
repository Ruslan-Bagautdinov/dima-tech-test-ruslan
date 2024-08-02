from fastapi import APIRouter, Depends
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from database.postgre_db import get_session
from security import refresh_token

router = APIRouter()


@router.post("/refresh_token", description="""
Конечная точка `/refresh_token` предназначена для обновления Access Token с использованием Refresh Token. После истечения срока действия Access Token (30 минут), используйте эту конечную точку для получения нового Access Token.

- **Refresh Token**: Передайте Refresh Token в теле запроса для обновления Access Token.

""")
async def refresh(refresh_token_str: str, session: AsyncSession = Depends(get_session)):
    logger.info("Attempting to refresh token")
    result = await refresh_token(refresh_token_str, session)
    logger.info("Token refreshed successfully")
    return result
