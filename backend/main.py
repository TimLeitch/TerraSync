from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from models.user import UserCreate, UserBase
from utils.security import hash_password, verify_password
from utils.local_token import create_access_token

# Database connection


async def get_db():
    print("Connecting to MongoDB")
    client = AsyncIOMotorClient("mongodb://localhost:27017/")
    db = client.get_database("test_db")
    print(f"Connected to database: {db.name}")
    try:
        yield db
    finally:
        print("Closing MongoDB connection")
        client.close()


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust the port if necessary
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "TerraSync"}


@app.post("/register", response_model=UserBase)
async def register_user(user: UserCreate, db=Depends(get_db)):
    existing_user = await db["users"].find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = hash_password(user.password)
    user_dict = user.dict()
    user_dict["hashed_password"] = hashed_password
    del user_dict["password"]

    # pylint: disable=no-member
    await db["users"].insert_one(user_dict)
    return {"username": user.username, "email": user.email}


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    user = await db["users"].find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Pass the user's group to the token creation function
    access_token = create_access_token(
        data={"sub": user["username"]}, groups=user.get("groups"))
    return {"access_token": access_token, "token_type": "bearer"}
