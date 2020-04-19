#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."


function pipeline {
	python -m colinthecomputer.saver run-saver  'postgresql://colin:password@127.0.0.1:5432/colin' 'rabbitmq://127.0.0.1:5672/' &
	pid[0]=$!; sleep 1; python -m colinthecomputer.parsers run-parser 'pose' 'rabbitmq://127.0.0.1:5672/' &
	pid[1]=$!; python -m colinthecomputer.parsers run-parser 'color_image' 'rabbitmq://127.0.0.1:5672/' &
	pid[2]=$!; python -m colinthecomputer.parsers run-parser 'depth_image' 'rabbitmq://127.0.0.1:5672/' &
	pid[3]=$!; python -m colinthecomputer.parsers run-parser 'feelings' 'rabbitmq://127.0.0.1:5672/' &
	pid[4]=$!; sleep 1; python -m colinthecomputer.server run-server 'rabbitmq://127.0.0.1:5672/' &
	pid[5]=$!; sleep 1; python -m colinthecomputer.client upload-sample ~/sample.mind.gz &
	pid[6]=$!; python -m colinthecomputer.api run-server -d 'postgresql://colin:password@127.0.0.1:5432/colin' &
	pid[7]=$!; python -m colinthecomputer.gui run-server &
	pid[8]=$!
	trap "kill ${pid[0]} ${pid[1]} ${pid[2]} ${pid[3]} ${pid[4]} ${pid[5]} ${pid[6]} ${pid[7]} ${pid[8]}; exit 1" INT
	wait
}

function main {
	echo 'starting pipeline...'
	echo 'API available at localhost:5000'
	echo 'GUI available at localhost:8080'
	pipeline &> '/dev/null'
}


main "$@"