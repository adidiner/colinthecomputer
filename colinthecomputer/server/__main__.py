import click
import sys
import os

from . import run_server
from .publisher import Publisher

@click.group()
def main():
    pass


@main.command('run-server')
@click.option('-h', '--host', default='0.0.0.0', type=str)
@click.option('-p', '--port', default=8000, type=int)
@click.argument('mq_url', type=str)
def cli_run_server(host, port, mq_url):
	# TODO - directory is env var
    publish = Publisher(mq_url, '/home/user/colinfs/raw_data').publish
    run_server(host=host, port=port, publish=publish)


if __name__ == '__main__':
    main(prog_name='colin-the-computer')