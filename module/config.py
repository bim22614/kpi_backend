import os
from dotenv import load_dotenv

load_dotenv()


PROPAGATE_EXCEPTIONS = True
FLASK_DEBUG = True
SQLALCHEMY_DATABASE_URI = f'postgresql://{os.environ.get("DB_USER")}:{os.environ.get("DB_PASSWORD")}@172.21.0.2:{os.environ.get("DB_PORT")}/{os.environ.get("DB_NAME")}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
API_TITLE = "Finance REST API"
API_VERSION = "v1"
OPENAPI_VERSION = "3.0.3"
OPENAPI_URL_PREFIX = "/"
OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
