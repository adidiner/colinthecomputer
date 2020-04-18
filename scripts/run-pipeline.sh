#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."


function pipeline {
	python -m colinthecomputer.saver run-saver  'postgresql://colin:password@127.0.0.1:5432/colin' 'rabbitmq://127.0.0.1:5672/' &
	sleep 1; python -m colinthecomputer.parsers run-parser 'pose' 'rabbitmq://127.0.0.1:5672/' &
	python -m colinthecomputer.parsers run-parser 'color_image' 'rabbitmq://127.0.0.1:5672/' &
	python -m colinthecomputer.parsers run-parser 'depth_image' 'rabbitmq://127.0.0.1:5672/' &
	python -m colinthecomputer.parsers run-parser 'feelings' 'rabbitmq://127.0.0.1:5672/' &
	sleep 1; python -m colinthecomputer.server run-server 'rabbitmq://127.0.0.1:5672/' &
	sleep 1; python -m colinthecomputer.client upload-sample ~/sample.mind.gz &
	python -m colinthecomputer.api run-server -d 'postgresql://colin:password@127.0.0.1:5432/colin' &
	python -m colinthecomputer.gui run-server

}

function main {
	pipeline > '/dev/null'
}


main "$@"