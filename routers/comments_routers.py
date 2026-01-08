from fastapi import APIRouter, Depends, Form
from uuid import UUID

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.post("/posts/{post_id}/comments")
def add_comment(post_id: UUID, content: str = Form(...)):
    # TODO: Implement add comment
    return {"message": "Comment added"}

@router.get("/posts/{post_id}/comments")
def list_comments(post_id: UUID, page: int = 1, limit: int = 10):
    # TODO: Implement list comments
    return {"comments": []}

@router.delete("/{comment_id}")
def delete_comment(comment_id: UUID):
    # TODO: Implement delete comment
    return {"message": "Comment deleted"}
