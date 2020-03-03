import click
import sys

from . import run_server
from .publisher import produce_publisher

@click.group()
def main():
    pass


@main.command('run-server')
@click.option('-h', '--host', default='127.0.0.1', type=str)
@click.option('-p', '--port', default=8000, type=int)
@click.argument('mq_url', type=str)
def cli_run_server(host, port, mq_url):
    publish = produce_publisher(mq_url)
    run_server(host=host, port=port, publish=publish)

def dummy_publish(message):
    print(message)

if __name__ == '__main__':
    main(prog_name='colin-the-computer')