#!/bin/bash
./manage.py migrate
if [[ -v DJANGO_SUPERUSER_USERNAME ]]
then
    echo "Creating Super User"
    ./manage.py createsuperuser --noinput
fi
./manage.py runserver 0.0.0.0:8000
