from fastapi import APIRouter, File, Depends

from app.plots.enums import Shapes
from app.users.api_models.user import User
from app.users.services.user import AuthService
from app.plots.services import rcs

router = APIRouter()


@router.get('/rcs')
async def rcs(z: float, shape: Shapes, user: User = Depends(AuthService.get_current_user)) -> File:
    return rcs.get_plot(z=z, shape=shape)
