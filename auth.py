#authentication

import bcrypt
from datetime import datetime, timedelta
from jose import JWTError, jwt

#PHASE 1: PASSWORD HASHING

#Hashing a plain password
def hash_password(password: str)->str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

#Check password on log-in (will be used in phase 2)
def verify_password(plain_password:str,hashed_password:str)->bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'),hashed_password.encode('utf-8'))

#PHASE 2: JWT Token Functions
SECRET_KEY = "your_secret_key" #can use os.environ later for security
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

def create_access_token(data: dict, expires_delta: timedelta | None=None):
    to_encode=data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str, credentials_exception):
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception