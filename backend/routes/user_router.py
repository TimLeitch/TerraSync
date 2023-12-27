from fastapi import APIRouter, HTTPException, Depends
from models.user import UserCreate, UserBase
from utils.security import hash_password
from utils.db import get_db, get_admin_db
router = APIRouter()


@router.post("/register", response_model=UserBase)
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
