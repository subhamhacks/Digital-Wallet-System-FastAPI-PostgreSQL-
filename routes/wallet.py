from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from dependencies import get_db, get_current_user
from models import User, Wallet, Transaction
from schemas import WalletTransactionSchema, BalanceResponse, WalletActionResponse, PaySchema, TransactionSchema
import requests
import os
from dotenv import load_dotenv

load_dotenv()
CURRENCY_API_KEY = os.getenv("CURRENCY_API_KEY")

router = APIRouter()

# Get current wallet balance (can be in another currency)
@router.get("/wallet/balance", response_model=BalanceResponse)
def get_balance(currency: str = None, current_user: User = Depends(get_current_user)):
    balance = current_user.wallet.balance

    if currency and currency.upper() != "INR":
        response = requests.get(
            f"https://api.currencyapi.com/v3/latest?apikey={CURRENCY_API_KEY}&base_currency=INR"
        )
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Currency conversion service unavailable")

        rates = response.json().get("data", {})
        rate = rates.get(currency.upper())

        if not rate:
            raise HTTPException(status_code=400, detail="Invalid or unsupported currency")

        converted_balance = round(balance * rate["value"], 2)
        return {"balance": converted_balance, "currency": currency.upper()}

    return {"balance": balance}

# Deposit money
@router.post("/wallet/Fund", response_model=WalletActionResponse)
def deposit(
    transaction: WalletTransactionSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if transaction.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")

    if not current_user.wallet:
        current_user.wallet = Wallet(user_id=current_user.id, balance=0.0)
        db.add(current_user.wallet)
        db.commit()
        db.refresh(current_user.wallet)

    current_user.wallet.balance += transaction.amount
    db.commit()
    db.refresh(current_user.wallet)

    # transaction log
    txn = Transaction(
        user_id=current_user.id,
        kind="credit",
        amount=transaction.amount,
        updated_bal=current_user.wallet.balance,
        note="Wallet funded"
    )
    db.add(txn)
    db.commit()

    return WalletActionResponse(message="Deposit Successful", balance=current_user.wallet.balance)

# Pay another user
@router.post("/wallet/pay", response_model=WalletActionResponse)
def pay_user(
    payload: PaySchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if payload.amt <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than 0")

    if not current_user.wallet or current_user.wallet.balance < payload.amt:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    recipient = db.query(User).filter(User.username == payload.to).first()

    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")

    if recipient.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot transfer to yourself")

    if not recipient.wallet:
        recipient.wallet = Wallet(user_id=recipient.id, balance=0.0)
        db.add(recipient.wallet)
        db.commit()
        db.refresh(recipient.wallet)

    # Transfer the amount
    current_user.wallet.balance -= payload.amt
    recipient.wallet.balance += payload.amt

    # Log both transactions
    db.add_all([
        Transaction(user_id=current_user.id, kind="debit", amount=payload.amt,
                    updated_bal=current_user.wallet.balance, note=f"To {recipient.username}"),
        Transaction(user_id=recipient.id, kind="credit", amount=payload.amt,
                    updated_bal=recipient.wallet.balance, note=f"From {current_user.username}")
    ])

    db.commit()
    db.refresh(current_user.wallet)

    return WalletActionResponse(
        message=f"Transferred ₹{payload.amt} to {recipient.username}",
        balance=current_user.wallet.balance
    )

# View transaction history
@router.get("/stmt", response_model=list[TransactionSchema])
def get_transaction_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    transactions = (
        db.query(Transaction)
        .filter(Transaction.user_id == current_user.id)
        .order_by(Transaction.timestamp.desc())
        .all()
    )
    return [
        TransactionSchema(
            kind=t.kind,
            amt=t.amount,
            updated_bal=t.updated_bal,
            timestamp=t.timestamp
        )
        for t in transactions
    ]
