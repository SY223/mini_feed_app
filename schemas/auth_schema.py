from pydantic import BaseModel, EmailStr, UUID4, Field
from datetime import datetime
from typing import Optional, Set, List

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
    #additional fields initiated by the Users resource
    display_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    updated_at: Optional[datetime] = None

    followers: Set[UUID4] = Field(default_factory=set)
    
    following: Set[UUID4] = Field(default_factory=set)

class LoginRequest(BaseModel):
    username_or_email: str
    password: str

class TokenRefreshRequest(BaseModel):
    refresh_token: str

