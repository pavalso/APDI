#!/bin/bash

export BLOB_STORAGE_FOLDER=${BLOB_STORAGE_FOLDER:-storage}

export BLOB_SERVER=blob_server

export RESULT=$( docker container inspect -f '{{.State.Running}}' ${BLOB_SERVER} 2>/dev/null )

if [ "${RESULT}" == "true" ]; then
    echo "${BLOB_SERVER} is already running"
    exit 1
fi

export PORT=${BLOB_SERVICE_PORT:-3002}

export AUTH_SERVER_URL=${AUTH_SERVER_URL:-http://host.docker.internal:3001}

docker run -p $PORT:$PORT \
            -e BLOB_STORAGE_FOLDER=${BLOB_STORAGE_FOLDER} \
            -e AUTH_SERVER_URL=${AUTH_SERVER_URL} \
            -v ./${BLOB_STORAGE_FOLDER}:/APDI/${BLOB_STORAGE_FOLDER} \
            -u 1000:1000 \
            --cpus=1 \
            --memory=2g \
            --rm \
            --name ${BLOB_SERVER} \
            ${BLOB_SERVER}
