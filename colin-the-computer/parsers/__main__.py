import click
import sys

from .mq_consumer import run_parser

@click.group()
def main():
    pass


@main.command('run-parser')
@click.argument('parser', type=str)
@click.argument('mq_url', type=str)
def cli_run_parser(parser, mq_url):
    run_parser(parser, mq_url)

def dummy_publish(message):
    print(message)

if __name__ == '__main__':
    main(prog_name='colin-the-computer')