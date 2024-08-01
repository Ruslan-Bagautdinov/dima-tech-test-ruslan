from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from loguru import logger
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from config import (ALGORITHM,
                    SECRET_KEY,
                    ACCESS_TOKEN_EXPIRE_MINUTES)
from database.crud import get_user_by_email
from database.postgre_db import get_session

security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: timedelta):
    logger.info("Creating access token")
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta):
    logger.info("Creating refresh token")
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    logger.info("Verifying password")
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(session: AsyncSession, email: str, password: str):
    logger.info(f"Authenticating user with email: {email}")
    user = await get_user_by_email(session, email)
    if not user or not verify_password(password, user.hashed_password):
        logger.warning(f"Authentication failed for user with email: {email}")
        return False
    return user


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security),
                           session: AsyncSession = Depends(get_session)):
    logger.info("Getting current user")
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        user = await get_user_by_email(session, email)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return user
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")


async def refresh_token(refresh_token_str: str, session: AsyncSession = Depends(get_session)):
    logger.info("Refreshing token")
    try:
        payload = jwt.decode(refresh_token_str, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        user = await get_user_by_email(session, email)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email, "id": user.id, "role": user.role},
            expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
