#!/bin/bash

wait_ready() {
    for i in {1..20}; do
        curl -s $1 > /dev/null
        if [ $? -eq 0 ]; then
            echo "$1 is ready"
            return
        fi
        sleep 1
    done
}

python3 test/auth_mock/auth_mock.py &

export AUTH_PID=$!

trap "kill $AUTH_PID; ./scripts/stop" EXIT

wait_ready https://auth.apiweb.com/

export AUTH_SERVER_URL=https://auth.apiweb.com/

./scripts/run &

wait_ready https://blobs.apiweb.com/

echo "Running tests"

python3 gentraf/gentraf https://blobs.apiweb.com/
