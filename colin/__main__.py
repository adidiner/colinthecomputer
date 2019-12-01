import click, sys

from . import upload_thought, run_server, run_webserver


@click.group()
def main():
	pass


def _parse_address(address):
	address = address.split(':')
	return (address[0], int(address[1]))


@main.command('upload')
@click.argument('address', type=str)
@click.argument('user', type=int)
@click.argument('thought', type=str)
def upload(address, user, thought):
	upload_thought(_parse_address(address), user, thought)


@main.command('serve')
@click.argument('address', type=str)
@click.argument('data', type=str)
def serve(address, data):
	run_server(_parse_address(address), data)


@main.command('webserve')
@click.argument('address', type=str)
@click.argument('data', type=str)
def webserve(address, data):
	run_webserver(_parse_address(address), data)


if __name__ == '__main__':
    try:
       	main()
    except Exception as error:
        print(f'ERROR: {error}')
        sys.exit(1)