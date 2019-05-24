#!/bin/sh
set -eux
coverage run --branch --omit=*/site-packages/*,poradnia/*/migrations/*.py "$@"
coveralls
