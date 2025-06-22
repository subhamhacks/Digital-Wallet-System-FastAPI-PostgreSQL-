from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from auth import verify_password

security = HTTPBasic()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency to get the current user using Basic Auth
def get_current_user(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)) -> User:
    user = db.query(User).filter(User.username == credentials.username).first()
    if user and verify_password(credentials.password, user.password):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Basic"},
    )