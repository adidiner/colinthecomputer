import click

from . import parsers
from .worker import Worker


@click.group()
def main():
    pass


@main.command('parse')
@click.argument('topic', type=str)
@click.argument('data', type=str)
def cli_parse(topic, data):
    with open(data, 'r') as file:
        data = file.read()
    print(parsers[topic](data))


@main.command('run-parser')
@click.argument('parser', type=str)
@click.argument('mq_url', type=str)
def cli_run_parser(parser, mq_url):
    work = Worker(mq_url).work
    work(parsers[parser], parser)


if __name__ == '__main__':
    main(prog_name='colinthecomputer')
