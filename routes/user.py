from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from schemas import RegisterSchema
from auth import hash_password

router = APIRouter()

#DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Register Endpoint
@router.post("/register",status_code=201)
def register_user(user: RegisterSchema,db:Session=Depends(get_db)):
    #check if username exist
    existing = db.query(User).filter(User.username==user.username).first()
    if existing:
        raise HTTPException(status_code=400,detail="Username already exists")
    
    #Hash password
    hashed_password=hash_password(user.password)

    #create and store the user
    new_user=User(username=user.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registeration Succesfull."}
