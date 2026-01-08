#entry point for FastAPI
from fastapi import FastAPI
from routers.auth_routers import router as auth_router
from routers.users_routers import router as users_router
from routers.posts_routers import router as posts_router
from routers.feed_routers import router as feed_router
from routers.likes_routers import router as likes_router
from routers.comments_routers import router as comments_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(posts_router, prefix="/posts", tags=["Posts"])
app.include_router(feed_router, prefix="/feed", tags=["Feed"])
app.include_router(likes_router, tags=["Likes"])
app.include_router(comments_router, tags=["Comments"])

@app.get("/")
def root():
    return{"message": "A mini social feed API working perfectly!"}