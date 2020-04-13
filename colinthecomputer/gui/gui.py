from flask import Flask, render_template, send_from_directory
import os

API_HOST = '127.0.0.1'
API_PORT = 8000


gui = Flask(__name__,
            static_folder='gui-react/build/static',
            template_folder='gui-react/build')


"""@gui.route('/', defaults={'path': ''})
@gui.route('/<path:path>')
def serve_react(path):
    api_root = f"{API_HOST}:{API_PORT}"
    return render_template("index.html", api_root=api_root)"""

@gui.route('/', defaults={'path': ''})
@gui.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists("gui-react/build/static/" + path):
        return send_from_directory('gui-react/build/static', path)
    else:
        return send_from_directory('gui-react/build/static', 'index.html')

def run_server(host, port, api_host, api_port):
    global API_HOST, API_PORT
    API_HOST = api_host
    API_PORT = api_port
    gui.run(host=host, port=port)