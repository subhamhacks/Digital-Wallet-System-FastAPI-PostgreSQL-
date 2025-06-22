from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import User, Product, Transaction
from dependencies import get_db, get_current_user
from schemas import ProductCreateSchema, ProductAddResponse,ProductSchema, BuyProductSchema

router = APIRouter()

@router.post("/product", response_model=ProductAddResponse, status_code=201)
def add_product(
    product: ProductCreateSchema,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    new_product = Product(
        name=product.name,
        price=product.price,
        description=product.description
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {"id": new_product.id, "message": "Product added"}

@router.get("/product",response_model=list[ProductSchema])
def list_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

@router.post("/buy")
def buy_product(
    payload: BuyProductSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Fetch product
    product = db.query(Product).filter(Product.id == payload.product_id).first()
    if not product:
        raise HTTPException(status_code=400, detail="Invalid product")

    # 2. Check balance
    if not current_user.wallet or current_user.wallet.balance < product.price:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    # 3. Deduct price from wallet
    current_user.wallet.balance -= product.price
    db.commit()
    db.refresh(current_user.wallet)

    # 4. Record transaction
    txn = Transaction(
        user_id=current_user.id,
        kind="debit",
        amount=product.price,
        updated_bal=current_user.wallet.balance
    )
    db.add(txn)
    db.commit()

    return {
        "message": "Product purchased",
        "balance": current_user.wallet.balance
    }