from fastapi import APIRouter, Depends
from uuid import UUID

router = APIRouter(prefix="/likes", tags=["Likes"])

@router.post("/posts/{post_id}/like")
def like_post(post_id: UUID):
    # TODO: Implement like post
    return {"message": "Post liked"}

@router.delete("/posts/{post_id}/like")
def unlike_post(post_id: UUID):
    # TODO: Implement unlike post
    return {"message": "Post unliked"}

@router.get("/posts/{post_id}/likes")
def list_likes(post_id: UUID):
    # TODO: Implement list likes
    return {"users": []}
