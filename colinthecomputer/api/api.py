from flask import Flask


from colinthecomputer.db_drivers import postgresql_driver

drivers = {'postgresql': postgresql_driver}
driver = drivers['postgresql']

api = Flask(__name__)

@api.route('/users')
def get_users():
    return driver.get_users()

def run_api_server(host, port, database_url):
    api.run(host=host, port=port)