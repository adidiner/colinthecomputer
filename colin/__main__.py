import click

from . import upload_thought, run_server, run_webserver

def _get_address(address):
	address = address.split(':')
	return (address[0], int(address[1]))

#TODO everything

if __name__ == '__main__':
    try:
       	pass
    except Exception as error:
        print(f'ERROR: {error}')
        sys.exit(1)