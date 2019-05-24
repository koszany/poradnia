#!/bin/sh
set -eux
python manage.py collectstatic --no-input
python manage.py migrate;

exec "$@"
