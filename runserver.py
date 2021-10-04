import uvicorn

from app import settings

if __name__ == "__main__":
    uvicorn.run(settings.APP_PATH,
                host=settings.HOST,
                port=settings.PORT,
                debug=settings.DEBUG,
                reload=settings.DEBUG)
