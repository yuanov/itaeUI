import os

APP_PATH = "app.main:app"
HOST = '127.0.0.1'
PORT = 9080
DEBUG = True
RELOAD = True
APP_DIRECTORY_PATH = os.path.join(os.getcwd(), 'app')

MONGODB_USERNAME = ''
MONGODB_PASSWORD = ''
MONGODB_HOSTNAME = 'localhost'
MONGODB_DATABASE = ''

ACCESS_TOKEN_EXPIRE_MINUTES = 1440
ALGORITHM = "HS256"
SECRET_KEY = 'n6z0NWstDGnwqtjSUG9zuuCw3Tg2un1uxSYEEPxSJDyMecOdbAPnBxoSADe3Nd4t'
