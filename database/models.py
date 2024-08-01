from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, validates

from database.postgre_db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    role = Column(String, default="user")

    accounts = relationship("Account", back_populates="owner")

    @validates('role')
    def validate_role(self, key, role):
        if role not in ['user', 'admin']:
            raise ValueError("Role must be 'user' or 'admin'")
        return role


class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    balance = Column(Float, default=0.0)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="accounts")
    payments = relationship("Payment", back_populates="account")


class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True)
    amount = Column(Float)
    account_id = Column(Integer, ForeignKey("accounts.id"))

    account = relationship("Account", back_populates="payments")
