#!/bin/sh

if [ "$DATABASE_ENGINE" = "django.db.backends.postgresql" ]
then
    echo "Waiting for $DATABASE_ENGINE..."

    while ! nc -z "$DATABASE_HOST" "$DATABASE_PORT"; do
      sleep 0.1
    done

    echo "$DATABASE_ENGINE started"
fi

python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input --clear

python populate.py

exec "$@"
