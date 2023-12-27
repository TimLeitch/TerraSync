from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from typing import Optional
from pydantic import BaseModel

# Use a strong secret key
SECRET_KEY = "ImNotVeryGoodAtMakingSuperSecretKeys,ButI'amOkayAtWrittingShittyCodeSometimes"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # or another duration
REFRESH_TOKEN_EXPIRE_MINUTES = 60


class TokenData(BaseModel):
    username: Optional[str] = None


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + \
        timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_access_token(data: dict, groups: str = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + \
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Add group information if provided
    if groups:
        to_encode.update({"groups": groups})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return token_data
