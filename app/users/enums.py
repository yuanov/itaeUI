from enum import Enum


class UserEnum(str, Enum):
    MONGODB_ID = '_id'
    ID = "id"
    FIRST_NAME = 'first_name'
    LAST_NAME = 'last_name'
    EMAIL = 'email'
    HASHED_PASSWORD = 'hashed_password'
