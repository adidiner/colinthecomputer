#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."


function main {
	cd colinthecomputer/gui/gui-react
	sudo npm install
	cd ../..
    python -m virtualenv .env --prompt "[colin] "
    find .env -name site-packages -exec bash -c 'echo "../../../../" > {}/self.pth' \;
    .env/bin/pip install -U pip
    .env/bin/pip install -r requirements.txt
}


main "$@"