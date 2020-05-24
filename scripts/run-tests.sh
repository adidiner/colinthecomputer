#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."


function main {
	sudo docker-compose -f docker-compose.testing.yml up -d &> '/dev/null'
	sleep 10
	pytest
	sudo docker-compose -f docker-compose.testing.yml down &> '/dev/null'
}


main "$@"