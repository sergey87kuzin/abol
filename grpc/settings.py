import os
import sys

from dotenv import load_dotenv

# Get the path to the directory this file is in
BASEDIR = os.path.abspath(os.path.dirname(__file__))

# Connect the path with your '.env' file name
load_dotenv(os.path.join(BASEDIR, '.env'))

ENVIRONMENT = os.getenv('ENVIRONMENT')

REAL_DATABASE_URL = os.getenv(
    "REAL_DATABASE_URL",
    default="postgresql://postgres:postgres@localhost:5432/abol",
)
if "pytest" in sys.modules:
    DB_NAME = os.getenv("DB_NAME_TEST")
    DB_USER = os.getenv("DB_USER_TEST")
    DB_PASSWORD = os.getenv("DB_PASSWORD_TEST")
    DB_HOST = os.getenv("DB_HOST_TEST")
    DB_PORT = os.getenv("DB_PORT_TEST")
else:
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")

DB_NAME_TEST = os.getenv("DB_NAME_TEST")
DB_USER_TEST = os.getenv("DB_USER_TEST")
DB_PASSWORD_TEST = os.getenv("DB_PASSWORD_TEST")
DB_HOST_TEST = os.getenv("DB_HOST_TEST")
DB_PORT_TEST = os.getenv("DB_PORT_TEST")
