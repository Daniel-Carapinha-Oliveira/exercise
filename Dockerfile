FROM python:3.12-alpine

# Create a non-root user and group
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /exercise

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev su-exec

RUN pip install uwsgi

COPY requirements/base.txt base.txt
COPY requirements/production.txt production.txt

RUN mkdir -p /exercise/exercise/media/img/
COPY static/imgs /exercise/exercise/media/img/

RUN pip install -r production.txt

COPY . /exercise

RUN sed -i 's/\r$//g' bin/*

RUN chmod +x bin/*

EXPOSE 8000