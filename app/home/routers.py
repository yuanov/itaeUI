from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

import os

from app.settings import APP_DIRECTORY_PATH

router = APIRouter()

static_dir = os.path.join(APP_DIRECTORY_PATH, 'home', 'static')
print(os.path.join(static_dir, 'templates'))

templates = Jinja2Templates(directory=os.path.join(static_dir, 'templates'))
@router.get('/home/{id}', response_class=HTMLResponse)
async def home(request: Request, id: str):
    return templates.TemplateResponse('home.html', {'request': request, 'id': id})
