#!/bin/sh
set -eux
npm install
npm rebuild node-sass
exec "$@"
