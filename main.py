#entry point for FastAPI
from fastapi import FastAPI
from routers.auth import router as auth_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Auth"])

@app.get("/")
def root():
    return{"message": "A mini social feed API"}