from fastapi import FastAPI

from app import settings
from app.users.routers import router as user_router
from app.home.routers import router as home_router

app = FastAPI(debug=settings.DEBUG)

app.include_router(home_router, tags=['Home'])
app.include_router(user_router, tags=['User'], prefix='/user')
