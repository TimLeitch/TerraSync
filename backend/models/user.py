from pydantic import BaseModel, EmailStr
from typing import List, Optional


class UserBase(BaseModel):
    username: str
    email: EmailStr
    groups: Optional[List[str]] = []


class UserCreate(UserBase):
    password: str


class UserInDB(UserBase):
    hashed_password: str
