FROM python:3.12-alpine

WORKDIR /exercise

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev

RUN pip install uwsgi

COPY requirements/base.txt base.txt
COPY requirements/production.txt production.txt

RUN mkdir -p /exercise/media/img/
COPY static/imgs /exercise/media/img/

RUN pip install -r production.txt

COPY . /exercise

RUN sed -i 's/\r$//g' bin/*

RUN chmod +x bin/*

EXPOSE 8000