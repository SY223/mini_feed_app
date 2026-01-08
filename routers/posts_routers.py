from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import Optional
from uuid import UUID

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/", status_code=201)
def create_post(title: Optional[str] = Form(None), content: str = Form(...), image: Optional[UploadFile] = File(None), visibility: Optional[str] = Form("public")):
    # TODO: Implement post creation
    return {"message": "Post created"}

@router.get("/")
def list_posts(page: int = 1, limit: int = 10, username: Optional[str] = None, q: Optional[str] = None, sort: Optional[str] = "created_at"):
    # TODO: Implement post listing
    return {"posts": []}

@router.get("/{post_id}")
def get_post(post_id: UUID):
    # TODO: Implement get single post
    return {"post": {}}

@router.patch("/{post_id}")
def update_post(post_id: UUID):
    # TODO: Implement update post
    return {"message": "Post updated"}

@router.delete("/{post_id}")
def delete_post(post_id: UUID):
    # TODO: Implement delete post
    return {"message": "Post deleted"}

