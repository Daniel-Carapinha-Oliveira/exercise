#!/bin/sh

mkdir -p /exercise/logs
touch /exercise/logs/django.log
chown -R appuser:appgroup /exercise/logs
chmod 664 /exercise/logs/django.log

# Fix ownership for volumes (needed on Linux)
chown -R appuser:appgroup /exercise/exercise/staticfiles
chown -R appuser:appgroup /exercise/exercise/media

python manage.py collectstatic --noinput

while true; do
  python manage.py migrate
  if [[ "$?" == "0" ]]; then
    break
  fi
  echo Migrate command failed, retrying in 5 secs...
  sleep 5
done

# run uwsgi as app user
exec su-exec appuser:appgroup uwsgi \
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