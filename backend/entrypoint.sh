#!/bin/sh

python manage.py wait_for_db

python manage.py create_super_user

python manage.py migrate

exec "$@"