from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

import os

from app.settings import APP_DIRECTORY_PATH

router = APIRouter()

templates = Jinja2Templates(directory=os.path.join(APP_DIRECTORY_PATH, 'home', 'templates'))


@router.get('/home', response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})
