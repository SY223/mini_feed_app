from pydantic import BaseModel, EmailStr, UUID4
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserPublic(UserBase):
    id: UUID4
    role: str
    created_at: datetime

class UserInDB(UserPublic):
    hashed_password: str

class LoginRequest(BaseModel):
    username_or_email: str
    password: str

class TokenRefreshRequest(BaseModel):
    refresh_token: str