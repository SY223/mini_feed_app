from uuid import UUID
from typing import Optional
from pydantic import BaseModel

class PostBase(BaseModel):
    title: Optional[str] = None
    content: str
    image_url: Optional[str] = None
    visibility: str = "public"

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None
    visibility: Optional[str] = None

class PostOut(PostBase):
    id: UUID
    user_id: UUID
    likes_count: int
    comments_count: int
    created_at: str
    updated_at: str

class CommentBase(BaseModel):
    content: str

class CommentOut(CommentBase):
    id: UUID
    user_id: UUID
    post_id: UUID
    created_at: str

class LikeOut(BaseModel):
    user_id: UUID
    post_id: UUID
    created_at: str
