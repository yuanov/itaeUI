from pydantic import EmailStr, BaseModel
from typing import Optional


class UserEmail(BaseModel):
    email: EmailStr


class UserLogin(UserEmail):
    password: str


class User(UserEmail):
    id: Optional[str]
    hashed_password: str
    first_name: Optional[str] = ''
    last_name: Optional[str] = ''
