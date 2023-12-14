#!/bin/bash

export BLOB_SERVER=blob_server

export RESULT=$( docker container inspect -f '{{.State.Running}}' ${BLOB_SERVER} 2>/dev/null )

if [ -z ${RESULT} ] || [ "${RESULT}" == "false" ]; then
    echo "${BLOB_SERVER} is not running"
    exit 1
fi

docker stop ${BLOB_SERVER}
