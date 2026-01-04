from fastapi import APIRouter, Depends, File, UploadFile, Form, Query
from fastapi import HTTPException
from typing import Optional, List
from schemas.posts_schema import PostCreate, PostPublic, PostUpdate
from routers.auth import get_current_user_dep, get_current_user_optional
from services.posts_services import create_post, list_public_posts, get_post_or_404, update_post, delete_post
from schemas.posts_schema import Visibility

router = APIRouter()


@router.post("/", response_model=PostPublic, status_code=201)
def create_new_post(
    title: Optional[str] = Form(None),
    content: str = Form(...),
    image: Optional[UploadFile] = File(None),
    visibility: Visibility = Form(Visibility.public),
    current_user=Depends(get_current_user_dep),
):
    post = create_post(current_user, title=title, content=content, image_file=image, visibility=visibility)
    return post


@router.get("/", response_model=List[PostPublic])
def get_posts(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    username: Optional[str] = Query(None),
    q: Optional[str] = Query(None),
    sort: Optional[str] = Query("created_at"),
):
    return list_public_posts(page=page, limit=limit, username=username, q=q, sort=sort)


@router.get("/{post_id}", response_model=PostPublic)
def get_single_post(post_id: str, current_user=Depends(get_current_user_optional)):
    post = get_post_or_404(post_id)
    # Public posts are always visible
    if post.visibility == Visibility.public:
        return post
    # For non-public posts we need a valid user
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required to view this post")
    # owner or admin allowed
    if str(current_user.id) == str(post.author_id) or getattr(current_user, "role", "user") == "admin":
        return post
    # followers-only: check if current_user is a follower of the author
    from databases.database import users_db
    author = None
    for u in users_db.values():
        if str(u.id) == str(post.author_id):
            author = u
            break
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    if post.visibility == Visibility.followers:
        # followers stored as set of UUIDs
        if str(current_user.id) in set(map(str, author.followers)):
            return post
        raise HTTPException(status_code=403, detail="Only followers can view this post")
    # private
    raise HTTPException(status_code=403, detail="Not allowed to view this post")


@router.patch("/{post_id}", response_model=PostPublic)
def patch_post(
    post_id: str,
    title: Optional[str] = Form(None),
    content: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    visibility: Optional[Visibility] = Form(None),
    current_user=Depends(get_current_user_dep),
):
    update = PostUpdate(title=title, content=content, visibility=visibility)
    post = update_post(post_id, current_user, update, image)
    return post


@router.delete("/{post_id}")
def remove_post(post_id: str, current_user=Depends(get_current_user_dep)):
    delete_post(post_id, current_user)
    return {"detail": "deleted"}
