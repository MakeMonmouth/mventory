#!/bin/sh

set -eux

env | grep MV

python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate

#unset MVENTORY_DEBUG

uwsgi --ini uwsgi.ini
