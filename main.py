#main

from fastapi import FastAPI
from models import Base
from database import engine
from routes import user,auth,wallet,product

app = FastAPI()

#create tables
Base.metadata.create_all(bind=engine)

#include user routes
app.include_router(user.router)

#include auth routes
app.include_router(auth.router)

#include wallet routes
app.include_router(wallet.router)

#include product routes
app.include_router(product.router)