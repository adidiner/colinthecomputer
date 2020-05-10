import click
import sys


from . import Saver
from .consumer import Consumer

@click.group()
def main():
    pass


@main.command('save')
@click.option('-d', '--database', default='postgresql://colin:password@127.0.0.1:5432/colin', type=str)
@click.argument('topic', type=str)
@click.argument('data', type=str)
def cli_save(database, topic, data):
    saver = Saver(database)
    with open(data, 'r') as file:
        data = file.read()
    saver.save(topic, data)


@main.command('run-saver')
@click.argument('db_url', type=str)
@click.argument('mq_url', type=str)
def cli_run_saver(db_url, mq_url):
    saver = Saver(db_url)
    consume = Consumer(mq_url).consume
    consume(saver.save)



if __name__ == '__main__':
    main(prog_name='colinthecomputer')