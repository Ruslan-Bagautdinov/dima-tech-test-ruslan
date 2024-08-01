from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional


class UserLogin(BaseModel):
    email: str
    password: str


class UserCreate(BaseModel):
    email: str
    hashed_password: str
    full_name: str
    role: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[str] = None

    @field_validator('role')
    def validate_role(cls, role):
        if role not in ['user', 'admin']:
            raise ValueError("Role must be 'user' or 'admin'")
        return role


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str


class WebhookPayload(BaseModel):
    transaction_id: str
    user_id: int
    account_id: int
    amount: float
    signature: str
