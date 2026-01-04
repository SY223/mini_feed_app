#entry point for FastAPI
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers.auth import router as auth_router
from routers.users import router as users_router
from routers.posts import router as posts_router

app = FastAPI()

# serve uploaded images
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(posts_router, prefix="/posts", tags=["Posts"])

@app.get("/")
def root():
    return{"message": "A mini social feed API"}