from enum import Enum
import uuid
from pydantic import BaseModel, EmailStr
from fastapi_users import schemas
from datetime import datetime

class Role(int, Enum):
    PATIENT = 1
    LAB_TECH = 2
    NURSE = 3
    DOCTOR = 4
    
class UserRead(schemas.BaseUser[uuid.UUID]):
    role_id: Role
    created_at: datetime
    updated_at: datetime

class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass

class UserUpdatePublic(schemas.CreateUpdateDictModel):
    password:str

class UserCreateRole(UserCreate):
    role_id: Role

class UserCreatePublic(schemas.CreateUpdateDictModel):
    email: EmailStr
    password: str
    
class UserOut(schemas.BaseUser):
    id: int

class UsersOut(BaseModel):
    data: list[UserOut]
    count: int
