#!/bin/sh
set -eux
python manage.py migrate;
exec "$@"
