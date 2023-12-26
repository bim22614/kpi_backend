FROM python:3.11.3-slim-bullseye


WORKDIR /app


COPY requirements.txt .


RUN python -m pip install -r requirements.txt


COPY . /app


CMD flask run -h 0.0.0.0 -p $PORT; exit 0
# CMD flask --app module:app run -h 0.0.0.0 -p $PORT
# CMD set FLASK_APP=module & set FLASK_ENV=development & flask run
# CMD [ "python3", "module/main.py" ]
