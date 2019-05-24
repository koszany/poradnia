#!/bin/bash
set -eux
docker build -t "${WEB_REPOSITORY_NAME}:${PYTHON_VERSION}" -f ./.contrib/docker/Dockerfile.web.production .;

docker tag "${WEB_REPOSITORY_NAME}:${PYTHON_VERSION}" "${WEB_REPOSITORY_NAME}:${TRAVIS_TAG}-${PYTHON_VERSION}";
docker push "${WEB_REPOSITORY_NAME}:${TRAVIS_TAG}-${PYTHON_VERSION}";
if [ "v$PYTHON_VERSION" == "v2.7" ]; then
	docker tag "${WEB_REPOSITORY_NAME}:${PYTHON_VERSION}" "${WEB_REPOSITORY_NAME}:latest"
	docker push "${DOCS_REPOSITORY_NAME}:latest"
fi;

