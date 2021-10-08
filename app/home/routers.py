from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

# templates = Jinja2Templates(directory=os.path.join(APP_DIRECTORY_PATH, 'home', 'templates'))


@router.get('/home', response_class=HTMLResponse)
async def home() -> str:
    return 'Welcome'
    # return templates.TemplateResponse('home.html', {'request': request})
