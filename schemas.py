#Schemas
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional

class RegisterSchema(BaseModel):
    username: str
    password: str 

class LoginSchema(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str ="bearer"

class WalletCreateSchema(BaseModel):
    initial_balance: Optional[float] = 0.0

class WalletResponse(BaseModel):
    id: int
    balance: float
    user_id: int

    model_config = ConfigDict(from_attributes=True)
 #This allows returning SQL Alchemy models directly

class UserResponse(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)

class WalletTransactionSchema(BaseModel):
    amount: float

class BalanceResponse(BaseModel):
    balance: float

class WalletActionResponse(BaseModel):
    message: str
    balance: float

class PaySchema(BaseModel):
    to: str
    amt: float

class BalanceResponse(BaseModel):
    balance: float
    currency: str = "INR"

class TransactionSchema(BaseModel):
    kind: str
    amt: float
    updated_bal: float
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

class ProductCreateSchema(BaseModel):
    name: str
    price: float
    description: str

class ProductAddResponse(BaseModel):
    id: int
    message: str

class ProductSchema(BaseModel):
    id: int
    name: str
    price: float
    description: str

    model_config = ConfigDict(from_attributes=True)

class BuyProductSchema(BaseModel):
    product_id: int
