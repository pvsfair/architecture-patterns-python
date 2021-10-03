# syntax=docker/dockerfile:1
FROM python:3.8-alpine as builder
WORKDIR /code
ENV FLASK_APP=app/app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

FROM builder as runner
EXPOSE 5000
CMD ["flask", "run"]

FROM builder as tester
COPY requirements-test.txt requirements-test.txt
RUN pip install -r requirements-test.txt
CMD ["pytest"]