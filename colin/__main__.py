import click
import sys

from . import upload_sample
from . import run_server as _run_server
from .utils import read as _read


@click.group()
def main():
    pass


@main.group()
def server():
    pass


@main.group()
def client():
    pass


def _parse_address(address):
    address = address.split(':')
    return (address[0], int(address[1]))


@client.command('run')
@click.argument('address', type=str)
@click.argument('sample', type=str)
def run_client(address, sample):
    upload_sample(_parse_address(address), sample)


@server.command('run')
@click.argument('address', type=str)
@click.argument('data', type=str)
def run_server(address, data):
    _run_server(_parse_address(address), data)


'''@main.command('webserve')
@click.argument('address', type=str)
@click.argument('data', type=str)
def webserve(address, data):
    run_webserver(_parse_address(address), data)'''


@main.command('read')
@click.argument('path', type=str)
def read(path):
    _read(path)


if __name__ == '__main__':
    try:
        main(prog_name='colin')
    except Exception as error:
        print(f'ERROR: {error}')
        sys.exit(1)
