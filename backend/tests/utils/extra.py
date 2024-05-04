import random
import string
from fastapi_users.schemas import BaseUser
import datetime
def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))

def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


user_data = [

    {"email": "dummy@dummy.com", "password": "dummy", "role_id": 1},
    {"email": "pat@pat.com", "password": "patpat", "role_id": 1},
    {"email": "lbth@lbth.com", "password": "lablab", "role_id": 2},
    {"email": "nur@nur.com", "password": "nurnur", "role_id": 3},
    {"email": "doc@doc.com", "password": "docdoc", "role_id": 4},
]

class UserDB(BaseUser):
    role_id: int

nurse_user = UserDB(
    id = "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    email="nurse@nurse.com",
    hashed_password="aaa",
    role_id=3,
    is_active=True,
    is_verified=True,
    is_superuser=False
)
