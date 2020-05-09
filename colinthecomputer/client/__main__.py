import click
import click
import sys

from . import upload_sample

@click.group()
def main():
    pass


@main.command('upload-sample')
@click.option('-h', '--host', default='127.0.0.1', type=str)
@click.option('-p', '--port', default=8000, type=int)
@click.argument('path', type=str)
def cli_upload_sample(host, port, path):
    upload_sample(host=host, port=port, path=path)


if __name__ == '__main__':
    main(prog_name='colinthecomputer')