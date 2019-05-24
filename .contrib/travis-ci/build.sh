#!/bin/sh
set -eux
if [ "$FLAKE_ONLY" == "true" ]; then
	docker build -f ./.contrib/docker/Dockerfile.flake8 -t flake8 .
	exit 0;
fi;

docker build --build-arg PYTHON_VERSION="$PYTHON_VERSION" -f ./.contrib/docker/Dockerfile.web.test -t "${WEB_REPOSITORY_NAME}:$PYTHON_VERSION" .
docker build -f ./.contrib/docker/Dockerfile.docs -t "${DOCS_REPOSITORY_NAME}:$PYTHON_VERSION" .
