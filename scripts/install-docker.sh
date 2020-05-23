#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."


function main {
	curl -fsSL https://get.docker.com -o scripts/get-docker.sh
	chmod +x scripts/get-docker.sh
	sudo sh scripts/get-docker.sh
	sudo curl -L "https://github.com/docker/compose/releases/download/1.23.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
	sudo chmod +x /usr/local/bin/docker-compose
}


main "$@"