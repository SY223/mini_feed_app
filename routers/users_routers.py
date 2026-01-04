from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status 
from typing import Optional, List
from uuid import UUID
from schemas.users_schemas import *
from schemas.auth_schema import *
from routers.auth_routers import get_current_user_dep
from datetime import datetime, timezone
from databases.database import users_db
from services.config import UPLOAD_DIR  
import os
import shutil

router = APIRouter()

AVATAR_UPLOAD_DIR = os.path.join(UPLOAD_DIR, "avatars")
os.makedirs(AVATAR_UPLOAD_DIR, exist_ok=True)

# -----------------------#
# Helper utilities       #
# -----------------------#
def get_user_by_username(username: str) -> UserInDB:
    user = users_db.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_user_by_id(user_id: str) -> Optional[UserInDB]:
    for user in users_db.values():
        if str(user.id) == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

def build_public_profile(user: UserInDB) -> UserProfilePublic:
    user_data = user.model_dump()
    # Calculate counts manually since they aren't stored as ints in UserInDB
    user_data["follower_count"] = len(user.followers)
    user_data["following_count"] = len(user.following)
    return UserProfilePublic(**user_data)

def build_follower_summary(user: UserInDB) -> FollowerSummary:
    return FollowerSummary(
        id=user.id,
        username=user.username,
        display_name=user.display_name,
        avatar_url=user.avatar_url
    )
# -----------------------#
# ENDPOINTS              #
# -----------------------#
@router.get("/{username}", response_model=UserProfilePublic)
def get_user_profile(username: str):
    one_user = get_user_by_username(username)
    return build_public_profile(one_user)

@router.patch("/me", response_model=UserProfilePublic)
def update_my_profile(
    display_name: Optional[str] = Form(None),
    bio: Optional[str] = Form(None),
    avatar: Optional[UploadFile] = File(None),
    current_user: UserInDB = Depends(get_current_user_dep)
):
    #locate the user in db
    user = users_db.get(current_user.username)
    if not user:
        raise HTTPException(status_code=404, detail="User session invalid")
    if display_name is not None:
        user.display_name = display_name
    if bio is not None:
        user.bio = bio
    if avatar:
        file_extension = os.path.splitext(avatar.filename)[1]
        file_name = f"{user.id}{file_extension}"
        file_path = os.path.join(AVATAR_UPLOAD_DIR, file_name)
        # Save the file to local storage
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(avatar.file, buffer)
        # Store the path in the user object
        user.avatar_url = f"/{file_path}"

    # 4. Update the 'updated_at' timestamp
    user.updated_at = datetime.now(timezone.utc)
    return build_public_profile(user)