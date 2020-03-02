import click
import sys


from . import run_parser
from . import parsers
from .consumer import produce_consumer

@click.group()
def main():
    pass


@main.command('run-parser')
@click.argument('parser', type=str)
@click.argument('mq_url', type=str)
def cli_run_parser(parser, mq_url):
    consume = produce_consumer(mq_url)
    consume(parsers[parser], parser)


if __name__ == '__main__':
    main(prog_name='colin-the-computer')