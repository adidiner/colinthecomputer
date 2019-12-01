import http.server
import pathlib
import flask

_INDEX_HTML = '''
<html>
    <head>
        <title>Brain Computer Interface</title>
    </head>
    <body>
        <ul>
            {users}
        </ul>
    </body>
</html>
'''
_USER_LINE_HTML = '''
<li><a href="/users/{user_id}">user {user_id}</a></li>
'''
_USER_HTML = '''
<html>
    <head>
        <title>Brain Computer Interface: User {user_id}</title>
    </head>
    <body>
        <table>
            {user_thoughts}
        </table>
    </body>
</html>
'''
_THOUGHT_HTML = '''
<tr>
	<td>{timestamp}</td>
	<td>{thought}</td>
</tr>
'''

#TODO flask

#@website.route('/')
def index():
	data_dir = pathlib.Path(DATA_DIR)
	users_html = []
	for user_dir in data_dir.iterdir():
		users_html.append(_USER_LINE_HTML.format(user_id=user_dir.name))
	return (200, _INDEX_HTML.format(users='\n'.join(users_html)))


#@website.route('/users/([0-9]+)')
def user(user_id):
	data_dir = pathlib.Path(DATA_DIR)
	for user_dir in data_dir.iterdir():
		if user_dir.name == user_id:
			break
	else:
		return (404, '')

	thoughts_html = []
	for thought in user_dir.iterdir():
		year, hour = thought.stem.split('_')
		timestamp = '{} {}'.format(year, ':'.join(hour.split('-')))
		thoughts_html.append(_THOUGHT_HTML.format(timestamp=timestamp, thought=thought.read_text()))
	return (200, _USER_HTML.format(user_id=user_id, user_thoughts='\n'.join(thoughts_html)))


def run_webserver(address, data_dir):
	global DATA_DIR
	DATA_DIR = data_dir
	website.run(address)
