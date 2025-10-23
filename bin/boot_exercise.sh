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

while true; do
  python manage.py loaddata user_fixture.json muscle_group_fixture.json muscle_fixture.json muscle_part_fixture.json exercise_fixture.json
  if [[ "$?" == "0" ]]; then
    break
  fi
  echo loaddata fixtures command failed, retrying in 5 secs...
  sleep 5
done


uwsgi --http "0.0.0.0:8000" --module exercise.wsgi --master --processes 4 --threads 2