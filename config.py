from os import getenv, path

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

BASE_DIR = path.dirname(path.abspath(__file__))

POSTGRES_HOST = getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = getenv('POSTGRES_PORT', '5432')
POSTGRES_USER = getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = getenv('POSTGRES_PASSWORD', 'password')
POSTGRES_DB = getenv('POSTGRES_DB', 'database')

DATABASE_URL = (f"postgresql+asyncpg"
                f"://{POSTGRES_USER}"
                f":{POSTGRES_PASSWORD}"
                f"@{POSTGRES_HOST}"
                f":{POSTGRES_PORT}"
                f"/{POSTGRES_DB}")

SYNC_DATABASE_URL = (f"postgresql"
                     f"://{POSTGRES_USER}"
                     f":{POSTGRES_PASSWORD}"
                     f"@{POSTGRES_HOST}"
                     f":{POSTGRES_PORT}"
                     f"/{POSTGRES_DB}")


SECRET_KEY = getenv('SECRET_KEY', 'secret-key')
ALGORITHM = getenv('ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '15'))
REFRESH_TOKEN_EXPIRE_MINUTES = int(getenv('REFRESH_TOKEN_EXPIRE_MINUTES', '10080'))
