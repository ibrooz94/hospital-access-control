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
