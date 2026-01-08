from fastapi import APIRouter, Depends
from typing import List
from uuid import UUID

router = APIRouter(prefix="/feed", tags=["Feed"])

@router.get("/")
def get_feed(page: int = 1, limit: int = 10):
    # TODO: Implement personalized feed
    return {"feed": []}
