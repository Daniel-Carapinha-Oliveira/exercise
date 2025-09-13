#!/bin/sh

python manage.py collectstatic

while true; do
  python manage.py migrate
  if [[ "$?" == "0" ]]; then
    break
  fi
  echo Migrate command failed, retrying in 5 secs...
  sleep 5
done

uwsgi --http "0.0.0.0:8000" --module exercise.wsgi --master --processes 4 --threads 2