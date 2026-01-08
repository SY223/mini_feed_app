from uuid import UUID
from typing import Optional
from pydantic import BaseModel

class FeedPost(BaseModel):
    id: UUID
    user_id: UUID
    title: Optional[str]
    content: str
    image_url: Optional[str]
    visibility: str
    created_at: str
    updated_at: str
    likes_count: int
    comments_count: int

class FeedOut(BaseModel):
    feed: list[FeedPost]
    page: int
    limit: int
    total: int
