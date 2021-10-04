# syntax=docker/dockerfile:1
FROM python:3.8-alpine as builder
WORKDIR /code
RUN apk add gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_APP=app/app.py

###### RUNNER ######
FROM builder as runner
CMD flask run -h 0.0.0.0 -p 5000

###### DEBUGGER ######
FROM builder as debugger
RUN pip install ptvsd

WORKDIR /code/
CMD python -m ptvsd --host 0.0.0.0 --port 5678 --wait --multiprocess -m flask run -h 0.0.0.0 -p 5000

###### TESTER ######
FROM builder as tester
COPY requirements-test.txt requirements-test.txt
RUN pip install -r requirements-test.txt
CMD ["pytest"]