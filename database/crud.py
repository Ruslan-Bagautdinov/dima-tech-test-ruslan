from loguru import logger
from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database.models import User, Account, Payment


async def get_user_by_email(session: AsyncSession, email: str):
    logger.info(f"Fetching user by email: {email}")
    query = select(User).where(User.email == email)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def get_user_by_id(session: AsyncSession, user_id: int):
    logger.info(f"Fetching user by ID: {user_id}")
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def get_all_users(session: AsyncSession):
    logger.info("Fetching all users")
    query = select(User)
    result = await session.execute(query)
    return result.scalars().all()


async def create_user(session: AsyncSession, user: User):
    logger.info(f"Creating new user with email: {user.email}")
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def update_user(session: AsyncSession, user_id: int, updates: dict):
    logger.info(f"Updating user with ID: {user_id}")
    query = update(User).where(User.id == user_id).values(**updates)
    await session.execute(query)
    await session.commit()


async def delete_user(session: AsyncSession, user_id: int):
    logger.info(f"Deleting user with ID: {user_id}")
    query = delete(User).where(User.id == user_id)
    await session.execute(query)
    await session.commit()


async def get_user_accounts(session: AsyncSession, user_id: int):
    logger.info(f"Fetching accounts for user ID: {user_id}")
    query = select(Account).where(Account.owner_id == user_id)
    result = await session.execute(query)
    return result.scalars().all()


async def get_user_payments(session: AsyncSession, user_id: int):
    logger.info(f"Fetching payments for user ID: {user_id}")
    query = select(Payment).join(Account).where(Account.owner_id == user_id)
    result = await session.execute(query)
    return result.scalars().all()


async def create_account(session: AsyncSession, account: Account):
    logger.info(f"Creating new account with ID: {account.id}")
    session.add(account)
    await session.commit()
    await session.refresh(account)
    return account


async def get_account_by_id(session: AsyncSession, account_id: int):
    logger.info(f"Fetching account by ID: {account_id}")
    query = select(Account).where(Account.id == account_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def update_account_balance(session: AsyncSession, account_id: int, amount: float):
    logger.info(f"Updating account balance for account ID: {account_id} with amount: {amount}")
    query = update(Account).where(Account.id == account_id).values(balance=Account.balance + amount)
    await session.execute(query)
    await session.commit()


async def create_payment(session: AsyncSession, payment: Payment):
    logger.info(f"Creating new payment with transaction ID: {payment.transaction_id}")
    session.add(payment)
    await session.commit()
    await session.refresh(payment)
    return payment


async def get_payment_by_transaction_id(session: AsyncSession, transaction_id: str):
    logger.info(f"Fetching payment by transaction ID: {transaction_id}")
    query = select(Payment).where(Payment.transaction_id == transaction_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()
