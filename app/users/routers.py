from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from app import settings
from app.users.api_models.user import UserLogin, User
from app.users.api_models.auth import Token
from app.users.services.user import UserService, AuthService

router = APIRouter()


@router.post('/register', response_model=Token, operation_id='register')
async def register(user: UserLogin) -> Token:
    await UserService.create(user)
    return AuthService.build_token(user)


@router.post("/login", response_model=Token, operation_id='login')
async def login(form_data: UserLogin) -> Token:
    user = await AuthService.authenticate_user(form_data.email, form_data.password)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = AuthService.create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")


@router.post("/login_swagger", response_model=Token)
async def login_swagger(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await AuthService.authenticate_user(form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = AuthService.create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/", response_model=User, operation_id='getMyUser')
async def get_my_user(current_user: User = Depends(AuthService.get_current_user)):
    return current_user
