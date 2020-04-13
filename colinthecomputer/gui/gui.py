from flask import Flask, render_template, send_from_directory
import os
from werkzeug.routing import BaseConverter


API_HOST = '127.0.0.1'
API_PORT = 8000

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


gui = Flask(__name__,
            static_folder='gui-react/build/static',
            template_folder='gui-react/build')
gui.url_map.converters['regex'] = RegexConverter


@gui.route('/', defaults={'path': ''})
@gui.route('/<path:path>')
def serve_react(path):
    api_root = f"http://{API_HOST}:{API_PORT}"
    return render_template("index.html", api_root=api_root)


@gui.route("/<regex(r'(.*?)\.(json|txt|png|PNG|ico|js)$'):file>", methods=["GET"])
def public(file):
    print(f"sending gui-react/build/{file}")
    return send_from_directory('gui-react/build', file)

"""@gui.route('/')
def serve_react(path):
    api_root = f"http://{API_HOST}:{API_PORT}"
    return render_template("index.html", api_root=api_root)
"""


"""@gui.route('/', defaults={'path': ''})
@gui.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists("gui-react/build/static/" + path):
        return send_from_directory('gui-react/build/static', path)
    else:
        return send_from_directory('gui-react/build/static', 'index.html')"""

def run_server(host, port, api_host, api_port):
    global API_HOST, API_PORT
    API_HOST = api_host
    API_PORT = api_port
    gui.run(host=host, port=port)