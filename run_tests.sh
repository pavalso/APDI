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

wait_ready http://auth.apiweb.com/

export AUTH_SERVER_URL=http://auth.apiweb.com/

./run &

wait_ready http://blobs.apiweb.com/

echo "Running tests"

python3 gentraf/gentraf http://blobs.apiweb.com/
