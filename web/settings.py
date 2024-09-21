import os
from dotenv import load_dotenv

# Get the path to the directory this file is in
BASEDIR = os.path.abspath(os.path.dirname(__file__))

# Connect the path with your '.env' file name
load_dotenv(os.path.join(BASEDIR, '.env'))

ENVIRONMENT = os.getenv('ENVIRONMENT')

REAL_DATABASE_URL = os.getenv(
    "REAL_DATABASE_URL",
    default="postgresql+asyncpg://postgres:postgres@localhost:5432/abol",
)

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    default="postgresql+asyncpg://posthres:postgres@localhost:5432/abol_test",
)
TEST_PASSWORD = os.getenv("TEST_PASSWORD")
SITE_DOMAIN = os.getenv("SITE_DOMAIN")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))
