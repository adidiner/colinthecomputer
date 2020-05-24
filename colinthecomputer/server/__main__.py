import click

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
    publish = Publisher(mq_url).publish
    run_server(host=host, port=port, publish=publish)


if __name__ == '__main__':
    main(prog_name='colinthecomputer')
