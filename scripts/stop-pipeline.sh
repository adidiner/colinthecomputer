#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."


function main {
	sudo docker-compose down
	sudo docker volume rm colinthecomputer_shared_data
}


main "$@"