import concurrent.futures
import asyncio
from fastapi import APIRouter, File, Depends

from app.plots.enums import Shapes
from app.users.api_models.user import User
from app.users.services.user import AuthService
from app.plots.services import rcs

router = APIRouter()


@router.get('/rcs')
async def get_rcs(shape: Shapes, z: float = 1, user: User = Depends(AuthService.get_current_user)) -> File:
    loop = asyncio.get_running_loop()
    with concurrent.futures.ProcessPoolExecutor() as pool:
        image = await loop.run_in_executor(pool, rcs.get_plot, z, shape)
    return image
