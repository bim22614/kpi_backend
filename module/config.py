import os

from dotenv import load_dotenv

load_dotenv()

PROPAGATE_EXCEPTIONS = True
FLASK_DEBUG = True
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
SQLALCHEMY_DATABASE_URI = f'postgresql://kpi_lab4_db_user:QEVgzwTuL7LiqLyFVUbinMa3HyUmSJVu@dpg-cma5h56n7f5s73b4s2ag-a.oregon-postgres.render.com/kpi_lab4_db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
API_TITLE = "Finance REST API"
API_VERSION = "v1"
OPENAPI_VERSION = "3.0.3"
OPENAPI_URL_PREFIX = "/"
OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
