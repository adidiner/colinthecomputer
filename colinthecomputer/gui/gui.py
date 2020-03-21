from flask import Flask, render_template, url_for, send_from_directory
import os

gui = Flask(__name__)

@gui.route('/')
def get_test():
    return render_template('test.html')

@gui.route('/users')
def get_users():
    return render_template('users.html')


'''@gui.route('/favicon.ico')
def favicon():
    print(os.path.join(gui.root_path, 'static'))
    return send_from_directory(gui.root_path,
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')
'''

def run_server(host, port, api_host, api_port):
    gui.run(host=host, port=port)
    #gui.add_url_rule('/favicon.ico',
    #             redirect_to=url_for('static', filename='favicon.ico'))
