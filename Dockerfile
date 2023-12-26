FROM python:3.11.3-slim-bullseye


WORKDIR /app


COPY requirements.txt .


RUN python -m pip install -r requirements.txt


COPY . /app


COPY wait-for-it.sh wait-for-it.sh


RUN chmod +x wait-for-it.sh


#CMD ./wait-for-it.sh localhost:5432 -t 30 -- flask run -h 0.0.0.0 -p $PORT
CMD flask run -h 0.0.0.0 -p $PORT

# CMD ["./wait-for-it.sh", "localhost:5432",  "-t", "10", "--" , "flask", "run", "-h", "0.0.0.0", "-p", "$PORT"]
# CMD ["flask", "run", "-h", "0.0.0.0", "-p", "$PORT"]
#CMD flask --app module:app run -h 0.0.0.0 -p $PORT
# CMD set FLASK_APP=module & set FLASK_ENV=development & flask run
# CMD [ "python3", "module/main.py" ]

