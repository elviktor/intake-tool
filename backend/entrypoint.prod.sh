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

# Evaluating passed command:
exec "$@"
