import hashlib

from fastapi import APIRouter, Depends, Query, HTTPException, status
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from config import SECRET_KEY
from database.crud import (get_payment_by_transaction_id,
                           get_account_by_id,
                           create_account,
                           create_payment,
                           update_account_balance
                           )
from database.models import Payment, Account
from database.postgre_db import get_session
from database.schemas import WebhookPayload

router = APIRouter()


async def verify_signature(payload: WebhookPayload):
    logger.info("Verifying webhook signature")
    secret_key = SECRET_KEY
    data_to_hash = f"{payload.account_id}{payload.amount}{payload.transaction_id}{payload.user_id}{secret_key}"
    calculated_signature = hashlib.sha256(data_to_hash.encode()).hexdigest()
    return calculated_signature == payload.signature


@router.post("/webhook")
async def process_webhook(payload: WebhookPayload, session: AsyncSession = Depends(get_session)):
    logger.info("Processing webhook")
    if not await verify_signature(payload):
        logger.warning("Invalid signature for webhook")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid signature")

    payment = await get_payment_by_transaction_id(session, payload.transaction_id)
    if payment:
        logger.warning(f"Transaction already processed for transaction ID: {payload.transaction_id}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Transaction already processed")

    account = await get_account_by_id(session, payload.account_id)
    if not account:
        logger.info(f"Creating new account for account ID: {payload.account_id}")
        new_account = Account(id=payload.account_id, owner_id=payload.user_id, balance=0.0)
        account = await create_account(session, new_account)

    logger.info(f"Creating new payment for transaction ID: {payload.transaction_id}")
    new_payment = Payment(
        transaction_id=payload.transaction_id,
        account_id=payload.account_id,
        amount=payload.amount
    )
    await create_payment(session, new_payment)
    await update_account_balance(session, payload.account_id, payload.amount)

    logger.info("Payment processed successfully")
    return {"detail": "Payment processed successfully"}


@router.get("/generate_webhook_json")
async def generate_webhook_json(
        transaction_id: str = Query(..., description="Transaction ID"),
        user_id: int = Query(..., description="User ID"),
        account_id: int = Query(..., description="Account ID"),
        amount: float = Query(..., description="Amount")
):
    data_to_hash = f"{account_id}{amount}{transaction_id}{user_id}{SECRET_KEY}"
    signature = hashlib.sha256(data_to_hash.encode()).hexdigest()

    response_json = {
        "transaction_id": transaction_id,
        "user_id": user_id,
        "account_id": account_id,
        "amount": amount,
        "signature": signature
    }

    return response_json





