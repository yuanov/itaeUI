from fastapi import FastAPI

from app import settings
from app.users.routers import router as user_router

app = FastAPI(debug=settings.DEBUG)

app.include_router(user_router, tags=['User'], prefix='/user')