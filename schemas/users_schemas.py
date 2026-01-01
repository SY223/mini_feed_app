from pydantic import BaseModel, UUID4, Field
from datetime import datetime
from typing import Optional, Set, List


# --- NEW: User Profile & Social Schemas ---
class UserProfileUpdate(BaseModel):
    display_name: Optional[str] = Field(None, max_length=50)
    bio: Optional[str] = Field(None, max_length=300)

class UserProfilePublic(BaseModel):
    username: str
    avatar_url: Optional[str] = None
    followers_count: int = 0
    following_count: int = 0
    #TimeStamps
    created_at: datetime
    updated_at: Optional[datetime] = None

# ------------------------- #
# Followers / Following models
# # -------------------------
class FollowerSummary(BaseModel):
    id: UUID4
    username: str
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None

class FollowersResponse(BaseModel):
    username: str
    followers: List[FollowerSummary]

class FollowingResponse(BaseModel):
    username: str
    following: List[FollowerSummary]
