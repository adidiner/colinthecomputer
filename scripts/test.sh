#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."


function main {
	sleep 100 && echo hi
}


main "$@"