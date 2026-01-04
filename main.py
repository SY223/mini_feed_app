#entry point for FastAPI
from fastapi import FastAPI
from routers.auth import router as auth_router
from routers.users import router as users_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(users_router, prefix="/users", tags=["Users"])

@app.get("/")
def root():
    return{"message": "A mini social feed API working perfectly!"}