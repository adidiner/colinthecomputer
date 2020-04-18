#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."


function main {
	cd colinthecomputer/gui/gui-react
	sudo npm install
}


main "$@"