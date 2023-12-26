import os

print(f'postgresql://{os.environ.get("DB_USER")}:{os.environ.get("DB_PASSWORD")}@db:{os.environ.get("DB_PORT")}/{os.environ.get("DB_NAME")}')
