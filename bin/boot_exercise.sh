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

while true; do
  python manage.py loaddata body_part_fixture.json
  if [[ "$?" == "0" ]]; then
    break
  fi
  echo loaddata body_part_fixture command failed, retrying in 5 secs...
  sleep 5
done

while true; do
  python manage.py loaddata muscle_fixture.json
  if [[ "$?" == "0" ]]; then
    break
  fi
  echo loaddata muscle_fixture command failed, retrying in 5 secs...
  sleep 5
done

while true; do
  python manage.py loaddata muscle_part_fixture.json
  if [[ "$?" == "0" ]]; then
    break
  fi
  echo loaddata muscle_part_fixture command failed, retrying in 5 secs...
  sleep 5
done

while true; do
  python manage.py loaddata exercise_fixture.json
  if [[ "$?" == "0" ]]; then
    break
  fi
  echo loaddata exercise_fixture command failed, retrying in 5 secs...
  sleep 5
done

uwsgi --http "0.0.0.0:8000" --module exercise.wsgi --master --processes 4 --threads 2