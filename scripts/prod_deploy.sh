#!/bin/sh

set -eux

python manage.py wait_for_db
#python manage.py collectstatic --noinput
python manage.py migrate

script="
from django.contrib.auth.models import User;

username = '$MVENTORY_ADMIN_USER';
password = '$MVENTORY_ADMIN_PASS';
email = '$MVENTORY_ADMIN_EMAIL';

if User.objects.filter(username=username).count()==0:
    User.objects.create_superuser(username, email, password);
    print('Superuser created.');
else:
    print('Superuser creation skipped.');
"
printf "$script" | python manage.py shell

uwsgi --ini uwsgi.ini
