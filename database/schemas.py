from pydantic import BaseModel


class UserLogin(BaseModel):
    email: str
    password: str


class UserCreate(BaseModel):
    email: str
    hashed_password: str
    full_name: str
    role: str


class UserUpdate(BaseModel):
    email: str
    full_name: str
    role: str


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
