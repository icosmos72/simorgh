#!/bin/bash -x

# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail

# http://stackoverflow.com/a/246128/586893
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# http://stackoverflow.com/a/2173421/586893
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT

# http://unix.stackexchange.com/a/132524
PORT=$(python2.7 -c 'import socket; s=socket.socket(); s.bind(("", 0)); print(s.getsockname()[1]); s.close()')

# http://stackoverflow.com/a/8351489/586893
# Retries a command a configurable number of times with backoff.
#
# The retry count is given by ATTEMPTS (default 5), the initial backoff
# timeout is given by TIMEOUT in seconds (default 1.)
#
# Successive backoffs double the timeout.

function with_backoff {
  local max_attempts=${ATTEMPTS-3}
  local timeout=${TIMEOUT-1}
  local attempt=0
  local exit_code=0

  while (( $attempt < $max_attempts )) ; do
    set +e
    "$@"
    exit_code=$?
    set -e

    if [[ $exit_code == 0 ]]
    then
      break
    fi

    echo "Failure! Retrying in $timeout second..." 1>&2
    sleep $timeout
    attempt=$(( attempt + 1 ))
    timeout=$(( timeout * 2 ))
  done

  if [[ $exit_code != 0 ]]
  then
    echo "Could not run command '$@' after ${attempt} attempts" 1>&2
  fi

  return $exit_code
}

function success {
	local green=`tput setaf 2`
	local reset=`tput sgr0`
	echo "${green}$@${reset}"
	return 0
}

function fail {
	local red=`tput setaf 1`
	local reset=`tput sgr0`
	echo "${red}$@${reset}"
	return 1
}

make -C ${DIR} reinstall

SIMORGH_DB=":MEMORY:" ${DIR}/venv/bin/python2.7 ${DIR}/venv/bin/simorgh_server --port ${PORT} &

if with_backoff curl http://127.0.0.1:${PORT}/data/temperature_measurements ; then
	success "Established connection with simorgh_server on PORT ${PORT}"
else
	fail "FAILED to establish connection with simorgh_server on PORT ${PORT}"
fi

test ! -f ~/.simorgh_db.json

function mock_temperature_data {
    cat <<EOF
{
  "type": "temperature measurement",
  "id": "$(uuidgen | tr '[:upper:]' '[:lower:]')",
  "session_id": "$(uuidgen | tr '[:upper:]' '[:lower:]')",
  "timestamp": $(python2.7 -c 'import time; print(time.time())'),
  "temperature": 21.0123,
  "manufacturer": "MCC",
  "device_model": "USB-TEMP",
  "serial_number": "001A92053B6ABB4131340023",
  "channel": 5,
  "PID": $$,
  "UID": ${UID},
  "process_name": "temperature_monitor.py",
  "commit_id": "$(git rev-parse HEAD)"
}
EOF
}

curl -H "Content-Type: application/json" \
     -X POST -d "$(mock_temperature_data)" \
     http://127.0.0.1:${PORT}/data/temperature_measurements

curl http://127.0.0.1:${PORT}/data/temperature_measurements | python -m json.tool

curl -H "Content-Type: application/json" \
     -X PUT -d "$(mock_temperature_data)" \
     http://127.0.0.1:${PORT}/data/temperature_measurements

curl http://127.0.0.1:${PORT}/data/temperature_measurements | python -m json.tool