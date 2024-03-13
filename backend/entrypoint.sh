#!/bin/sh

set -e

# activate our virtual environment here
. /opt/pysetup/.venv/bin/activate

echo "Let's go!"
#python manage.py flush --no-input
#python manage.py collectstatic --no-input
#python manage.py makemigrations
#python manage.py migrate
#echo "Migrations made"
#python manage.py makemigrations tracker
#python manage.py migrate tracker
#echo "Tracker Migrations made"
#python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL
python manage.py runserver "0.0.0.0:8000"

exec "$@"
