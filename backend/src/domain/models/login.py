from pydantic import BaseModel
from typing import Optional


class Login(BaseModel):
    password: str
    email: Optional[str] = None
    username: Optional[str] = None
