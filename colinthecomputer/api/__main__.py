import click
import sys


from . import run_api_server

@click.group()
def main():
    pass


@main.command('run-server')
@click.option('-h', '--host', default='127.0.0.1', type=str)
@click.option('-p', '--port', default=8000, type=int)
@click.option('-d', '--database', default='postgresql://colin:password@127.0.0.1:5432/colin', type=str)
def cli_run_api_server(host, port, database):
    run_api_server(host=host, port=port, database_url=database)


if __name__ == '__main__':
    main(prog_name='colinthecomputer')