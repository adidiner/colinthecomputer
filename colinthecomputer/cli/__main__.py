import click
import sys
import requests
from furl import furl
import functools
import urllib.request
import json


@click.group()
def main():
    pass

# https://stackoverflow.com/questions/52144383/using-a-python-click-cli-how-to-add-common-options-to-sub-commands-which-can
def network_options(f):
    options = [
        click.option('-h', '--host', default='127.0.0.1', type=str),
        click.option('-p', '--port', default=8000, type=int)
        ]
    return functools.reduce(lambda x, opt: opt(x), options, f)

def get_json(host, port, path):
    f = furl()
    f.set(scheme='http', host=host, port=port, path=path)
    r = requests.get(f.url)
    return r.json()

@main.command('get-users')
@network_options
def cli_get_users(host, port):
    print(get_json(host, port, 'users'))

@main.command('get-user')
@network_options
@click.argument('user_id', type=int)
def cli_get_user(host, port, user_id):
    print(get_json(host, port, f'users/{user_id}'))

@main.command('get-snapshots')
@network_options
@click.argument('user_id', type=int)
def cli_get_snapshots(host, port, user_id):
    print(get_json(host, port, f'users/{user_id}/snapshots'))

@main.command('get-snapshot')
@network_options
@click.argument('user_id', type=int)
@click.argument('snapshot_id', type=int)
def cli_get_snapshot(host, port, user_id, snapshot_id):
    print(get_json(host, port, f'users/{user_id}/snapshots/{snapshot_id}'))

@main.command('get-result')
@network_options
@click.option('-s', '--save', default=None, type=str)
@click.argument('user_id', type=int)
@click.argument('snapshot_id', type=int)
@click.argument('result', type=str)
def cli_get_result(host, port, save, user_id, snapshot_id, result):
    response = get_json(host, port, f'users/{user_id}/snapshots/{snapshot_id}/{result}')
    print(response)
    if save:
        path = response['path']
        f = furl()
        f.set(scheme='http', host=host, port=port, path=path)
        urllib.request.urlretrieve(f.url, save)



if __name__ == '__main__':
    main(prog_name='colinthecomputer')