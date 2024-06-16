import os
from pathlib import Path

Base_Dir = Path(__file__).parent

import dotenv
dotenv.load_dotenv(Path(Base_Dir.parent.parent, '.env'))


HTTP_PROTOCOL = 'http'
HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))

DATABASE = {
    'DRIVER': 'postgresql+asyncpg',
    'USER': os.getenv('DB_USER'),
    'PASSWORD': os.getenv('DB_PASSWORD'),
    'NAME': os.getenv('DB_NAME'),
    'HOST': os.getenv('DB_HOST'),
    'PORT': int(os.getenv('DB_PORT'))
}

TEST_DATABASE = {
    'DRIVER': 'postgresql+asyncpg',
    'USER': os.getenv('TEST_DB_USER'),
    'PASSWORD': os.getenv('TEST_DB_PASSWORD'),
    'NAME': os.getenv('TEST_DB_NAME'),
    'HOST': os.getenv('TEST_DB_HOST'),
    'PORT': int(os.getenv('TEST_DB_PORT'))
}


CATEGORY_KEY_SIZE = 4
