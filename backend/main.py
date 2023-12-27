
from routes import user_router, auth_router

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from models.user import UserCreate, UserBase
from utils.security import hash_password, verify_password
from utils.local_token import create_access_token, create_refresh_token

# Da

app = FastAPI()

app.include_router(user_router.router)
app.include_router(auth_router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],  # Adjust the port if necessary
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "TerraSync"}
