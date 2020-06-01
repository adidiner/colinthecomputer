#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."


function main {
	sudo apt-get update
	sudo apt-get install -y npm
	sudo npm install -g npm@latest
	cd colinthecomputer/gui/gui-react
	sudo npm install
	sudo npm install react react-dom react-router-dom bootstrap
	sudo npm run build
	cd ../..
}


main "$@"