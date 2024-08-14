import uuid
from enum import Enum
from pydantic import BaseModel, EmailStr, ConfigDict
from fastapi_users import schemas
from datetime import datetime

class Role(int, Enum):
    PATIENT = 1
    LAB_TECH = 2
    NURSE = 3
    DOCTOR = 4
    
class RoleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: Role
    name: str 

class UserRead(schemas.BaseUser[uuid.UUID]):
    role: RoleOut
    is_allowed: bool
    first_name: str | None
    last_name: str | None
    gender: str | None
    phone_number: str | None
    created_at: datetime
    updated_at: datetime

class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str
    gender: str
    phone_number: str

class UserUpdate(schemas.BaseUserUpdate):
    pass

class UserUpdatePublic(schemas.CreateUpdateDictModel):
    password:str

class UserCreateRole(UserCreate):
    role_id: Role

class UserCreatePublic(schemas.CreateUpdateDictModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    gender: str
    phone_number: str
    
class UserOut(schemas.BaseUser):
    id: int

class UsersOut(BaseModel):
    data: list[UserOut]
    count: int
