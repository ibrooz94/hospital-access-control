import bcrypt
import datetime as dt
from typing import Any
from datetime import datetime, timedelta
from joserfc import jwt

from .config import settings

ALGORITHM = {"alg": "HS256"}

def hash_password(password: str):
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(password = plain_password.encode('utf-8'), 
                          hashed_password = hashed_password.encode('utf-8'))

def create_access_token(subject: str | Any, expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.now(dt.UTC) + expires_delta
    else:
        expire = datetime.now(dt.UTC) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(ALGORITHM, to_encode, settings.SECRET_KEY,)
    return encoded_jwt
