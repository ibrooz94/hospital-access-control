import random
import string

from src.core.config import settings
from httpx import AsyncClient

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