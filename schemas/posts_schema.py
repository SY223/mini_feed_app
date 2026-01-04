from pydantic import BaseModel, UUID4, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class Visibility(str, Enum):
    public = "public"
    followers = "followers"
    private = "private"


class PostCreate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    content: str = Field(..., min_length=1)
    visibility: Optional[Visibility] = Visibility.public


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    content: Optional[str] = None
    visibility: Optional[Visibility] = None


class PostInDB(BaseModel):
    id: UUID4
    author_id: UUID4
    author_username: str
    title: Optional[str] = None
    content: str
    image_url: Optional[str] = None
    visibility: Visibility
    likes_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None


class PostPublic(PostInDB):
    pass
