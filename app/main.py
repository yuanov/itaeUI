from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app import settings
from app.users.routers import router as user_router
from app.home.routers import router as home_router
from app.plots.routers import router as plot_router

app = FastAPI(debug=settings.DEBUG)

app.include_router(home_router, tags=['Home'])
app.include_router(user_router, tags=['User'], prefix='/user')
app.include_router(plot_router, tags=['Plot'], prefix='/plot')

app.mount('/static', StaticFiles(directory='static'), name='static')
