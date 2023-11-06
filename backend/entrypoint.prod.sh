#!/bin/sh

#!/bin/sh

set -e

# activate our virtual environment here
. /opt/pysetup/.venv/bin/activate

# You can put other setup logic here 
echo "Let's go!"

# Experiment...
python manage.py flush --no-input
python manage.py migrate
python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL --password $DJANGO_SUPERUSER_PASSWORD

# You can put other setup logic here 
echo "Superuser created!"

# Evaluating passed command:
exec "$@"
