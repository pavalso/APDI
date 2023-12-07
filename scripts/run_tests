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

wait_ready http://localhost:5000

export AUTH_SERVER_URL=http://host.docker.internal:5000

./scripts/run &

wait_ready http://localhost:3002

echo "Running tests"

python3 gentraf/gentraf http://localhost:3002
