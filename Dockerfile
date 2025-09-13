FROM python:3.12-alpine

WORKDIR /exercise

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev

RUN pip install uwsgi

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /exercise

RUN sed -i 's/\r$//g' bin/*

RUN chmod +x bin/*

EXPOSE 8000