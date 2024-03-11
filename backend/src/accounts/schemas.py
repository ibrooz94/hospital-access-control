from enum import Enum
from pydantic import BaseModel

class Role(str, Enum):
    admin = 'admin'
    user = 'user'
    doctor = 'doctor'

class UserBase(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    is_active: bool | None = True
    is_superuser: bool = False

class UserCreate(UserBase):
    email: str
    password: str

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    hashed_password: str
