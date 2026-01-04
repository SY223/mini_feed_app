import uuid
import os
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import HTTPException
from schemas.posts_schema import PostInDB, PostCreate, PostUpdate, Visibility
from databases.database import posts_db

UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")


def _now():
    return datetime.now(timezone.utc)


def _save_image(upload_file) -> str:
    if not upload_file:
        return None
    # ensure upload dir
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    ext = os.path.splitext(upload_file.filename)[1]
    fname = f"{uuid.uuid4()}{ext}"
    path = os.path.join(UPLOAD_DIR, fname)
    with open(path, "wb") as f:
        contents = upload_file.file.read()
        f.write(contents)
    # return path relative to server root for static mount
    return f"/uploads/{fname}"


def create_post(author, title: Optional[str], content: str, image_file, visibility: Visibility):
    post_id = str(uuid.uuid4())
    image_url = _save_image(image_file) if image_file else None
    post = PostInDB(
        id=post_id,
        author_id=author.id,
        author_username=author.username,
        title=title,
        content=content,
        image_url=image_url,
        visibility=visibility,
        likes_count=0,
        created_at=_now(),
    )
    posts_db[post_id] = post
    return post


def get_post_or_404(post_id: str) -> PostInDB:
    p = posts_db.get(post_id)
    if not p:
        raise HTTPException(status_code=404, detail="Post not found")
    return p


def update_post(post_id: str, actor, update: PostUpdate, image_file):
    post = get_post_or_404(post_id)
    # owner required
    if str(actor.id) != str(post.author_id) and getattr(actor, "role", "user") != "admin":
        raise HTTPException(status_code=403, detail="Not allowed to edit this post")
    changed = False
    if update.title is not None:
        post.title = update.title
        changed = True
    if update.content is not None:
        post.content = update.content
        changed = True
    if update.visibility is not None:
        post.visibility = update.visibility
        changed = True
    if image_file is not None:
        post.image_url = _save_image(image_file)
        changed = True
    if changed:
        post.updated_at = _now()
        posts_db[str(post.id)] = post
    return post


def delete_post(post_id: str, actor):
    post = get_post_or_404(post_id)
    if str(actor.id) != str(post.author_id) and getattr(actor, "role", "user") != "admin":
        raise HTTPException(status_code=403, detail="Not allowed to delete this post")
    del posts_db[str(post.id)]
    return True


def list_public_posts(page: int = 1, limit: int = 10, username: Optional[str] = None, q: Optional[str] = None, sort: str = "created_at") -> List[PostInDB]:
    items = [p for p in posts_db.values() if p.visibility == Visibility.public]
    if username:
        items = [p for p in items if p.author_username == username]
    if q:
        qlower = q.lower()
        items = [p for p in items if qlower in (p.content or "").lower() or (p.title and qlower in p.title.lower())]
    if sort == "likes_count":
        items.sort(key=lambda x: x.likes_count, reverse=True)
    else:
        # default sort by created_at desc
        items.sort(key=lambda x: x.created_at, reverse=True)
    # pagination
    start = (page - 1) * limit
    end = start + limit
    return items[start:end]
