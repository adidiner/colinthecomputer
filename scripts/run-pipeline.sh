#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."


function pipeline {
	sudo docker-compose up -d
}

function main {
	echo 'Starting pipeline...'
	pipeline
	echo 'Please wait a few moments for everything to load'
	sleep 20
	echo 'API available at localhost:5000'
	echo 'GUI available at localhost:8080'
	echo 'Run a client to start the pipeline'
}


main "$@"