from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends
from passlib.context import CryptContext
from datetime import timedelta, datetime
from typing import Optional
from jose import JWTError, jwt

from app import settings
from app.db import user_collection
from app.users.enums import UserEnum
from app.users.api_models.user import UserLogin, User, UserEmail
from app.users.api_models.auth import Token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login_swagger")


class UserService:
    @staticmethod
    async def create(user: UserLogin) -> None:
        if await user_collection.find_one({UserEnum.EMAIL: user.email}) is not None:
            raise HTTPException(status_code=400,
                                detail='This email is already being used')

        hashed_password = AuthService.get_password_hash(user.password)
        user_db = User(email=user.email, hashed_password=hashed_password)
        await user_collection.insert_one(user_db.dict())

    @staticmethod
    async def get_user(email: str) -> User:
        user_dict = await user_collection.find_one({UserEnum.EMAIL: email})
        if user_dict is not None:
            user_dict[UserEnum.ID] = str(user_dict[UserEnum.MONGODB_ID])
            return User(**user_dict)


class AuthService:
    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

    @classmethod
    def build_token(cls, user) -> Token:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = AuthService.create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
        return Token(access_token=access_token, token_type="bearer")

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    @classmethod
    async def authenticate_user(cls, email: str, password: str):
        user = await UserService.get_user(email)
        if not user or not cls.verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @classmethod
    async def get_current_user(cls, token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = await UserService.get_user(email=email)
        if user is None:
            raise credentials_exception
        return user
