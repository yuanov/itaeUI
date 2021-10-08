import motor.motor_asyncio
from app import settings

login_str = f'{settings.MONGODB_USERNAME}:{settings.MONGODB_PASSWORD}@' if settings.MONGODB_USERNAME else ''

MONGO_DETAILS = f'mongodb://{login_str}{settings.MONGODB_HOSTNAME}:27017/{settings.MONGODB_DATABASE}'

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

user_collection = client.itaeUI.get_collection("users")
