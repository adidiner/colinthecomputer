#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."


function pipeline {
	sudo docker-compose up -d
}

function main {
	echo 'starting pipeline...'
	pipeline
	sleep 30
	echo 'API available at localhost:5000'
	echo 'GUI available at localhost:8080'
	echo 'run a client to start the pipeline'
}


main "$@"