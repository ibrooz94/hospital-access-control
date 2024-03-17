from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"

class TokenPayload(BaseModel):
    sub: int | None = None
