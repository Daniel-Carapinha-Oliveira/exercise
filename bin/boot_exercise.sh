#!/bin/sh

python manage.py collectstatic --noinput

while true; do
  python manage.py migrate
  if [[ "$?" == "0" ]]; then
    break
  fi
  echo Migrate command failed, retrying in 5 secs...
  sleep 5
done

uwsgi \
  --http 0.0.0.0:8000 \
  --module exercise.wsgi \
  --master \
  --processes 4 \
  --threads 2 \
  --vacuum \
  --harakiri 30 \
  --max-requests 1000 \
  --max-requests-delta 50 \
  --enable-threads \
  --uid appuser \
  --gid appgroup \
  --die-on-term