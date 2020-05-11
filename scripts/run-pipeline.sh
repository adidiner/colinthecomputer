#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."


function pipeline {
	sudo docker-compose up -d
}

function main {
	echo 'Starting pipeline...'
	pipeline
	echo 'Please wait a few moments for everything to load...'
	up=$(HEAD 127.0.0.1:5000/users | grep '200\ OK' | wc -l)
	while [ "$up" -eq "0" ]; do
		up=$(HEAD 127.0.0.1:5000/users | grep '200\ OK' | wc -l)
		sleep 1
	done
	echo 'API available at localhost:5000'
	up=$(HEAD 127.0.0.1:8080 | grep '200\ OK' | wc -l)
	while [ "$up" -eq "0" ]; do
		up=$(HEAD 127.0.0.1:8080 | grep '200\ OK' | wc -l)
		sleep 1
	done
	echo 'GUI available at localhost:8080'
	echo 'Run a client to start the pipeline'
}


main "$@"