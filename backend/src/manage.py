import uvicorn


from main import settings
from main.app import app


if __name__ == '__main__':
    uvicorn.run(
        app=app,
        host=settings.HOST,
        port=settings.PORT
    )

