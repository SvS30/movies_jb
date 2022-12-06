#!/bin/bash

set -xe

python manage.py makemigrations Movie Genre Auth UserActions

python manage.py migrate

echo "from django.contrib.auth.models import User; User.objects.create_superuser('adminroot', 'root@movies.com', 'adminroot123')" | python manage.py shell

python manage.py runserver 0.0.0.0:80