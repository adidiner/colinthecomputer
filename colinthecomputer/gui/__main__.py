import click
import sys


from . import run_server

@click.group()
def main():
    pass


@main.command('run-server')
@click.option('-h', '--host', default='127.0.0.1', type=str)
@click.option('-p', '--port', default=8080, type=int)
@click.option('-H', '--api-host', default='127.0.0.1', type=str)
@click.option('-P', '--api-port', default=5000, type=int)
def cli_run_server(host, port, api_host, api_port):
    run_server(host=host, port=port, api_host=api_host, api_port=api_port)


if __name__ == '__main__':
    main(prog_name='colinthecomputer')