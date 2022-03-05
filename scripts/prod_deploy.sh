#!/bin/sh

set -eux

python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate

unset MVENTORY_DEBUG

uwsgi --http-socket :9000 --workers 4 --master --enable-threads --module mventory.wsgi
