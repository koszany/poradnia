#!/bin/bash
set -eux
docker run --rm flake8

NETWORK_NAME="poradnia_network"
docker network create "$NETWORK_NAME"

MYSQL_NAME="poradnia_mysql"
docker run --rm -d --network "$NETWORK_NAME" \
	-e MYSQL_ROOT_PASSWORD="root" \
	-e MYSQL_DATABASE="poradnia" \
	--name "$MYSQL_NAME" \
	mysql:5.7 \
	--character-set-server=utf8 --collation-server=utf8_polish_ci;
sleep 10
function finish {
  docker stop "$MYSQL_NAME";
  docker network rm "$NETWORK_NAME";
}
docker logs "$MYSQL_NAME"
trap finish EXIT

export DATABASE_URL="mysql://root:root@poradnia_mysql/poradnia"
docker run --rm -it --network "$NETWORK_NAME" \
	-e TRAVIS -e TRAVIS_JOB_ID -e TRAVIS_BRANCH -e DATABASE_URL \
	"${WEB_REPOSITORY_NAME}:test" \
	 manage.py makemigrations --check --dry-run
docker run --rm -it --network "$NETWORK_NAME" \
	-e TRAVIS -e TRAVIS_JOB_ID -e TRAVIS_BRANCH -e DATABASE_URL \
	"${WEB_REPOSITORY_NAME}:test"

