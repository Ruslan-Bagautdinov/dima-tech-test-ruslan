from fastapi import APIRouter, Depends
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from database.postgre_db import get_session
from security import refresh_token

router = APIRouter()


@router.post("/refresh_token")
async def refresh(refresh_token_str: str, session: AsyncSession = Depends(get_session)):
    logger.info("Attempting to refresh token")
    result = await refresh_token(refresh_token_str, session)
    logger.info("Token refreshed successfully")
    return result
