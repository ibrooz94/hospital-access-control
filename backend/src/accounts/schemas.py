from enum import Enum
import uuid
from pydantic import BaseModel, EmailStr
from fastapi_users import schemas

class Role(str, Enum):
    admin = 'admin'
    user = 'user'
    doctor = 'doctor'
    
class UserRead(schemas.BaseUser[uuid.UUID]):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass

class UserCreatePublic(schemas.CreateUpdateDictModel):
    email: EmailStr
    password: str
    
class UserOut(schemas.BaseUser):
    id: int

class UsersOut(BaseModel):
    data: list[UserOut]
    count: int
