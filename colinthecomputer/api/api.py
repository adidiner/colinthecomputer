from flask import Flask
from furl import furl
import json


from colinthecomputer.db_drivers import postgresql_driver

drivers = {'postgresql': postgresql_driver}
driver = None

api = Flask(__name__)

@api.route('/users')
def get_users():
    return json.dumps(driver.get_users())

@api.route('/users/<int:user_id>')
def get_user_info(user_id):
    return json.dumps(driver.get_user_info(user_id))

@api.route('/users/<int:user_id>/snapshots')
def get_snapshots(user_id):
    return json.dumps(driver.get_snapshots(user_id))

@api.route('/users/<int:user_id>/snapshots/<int:snapshot_id>')
def get_snapshot_info(user_id, snapshot_id):
    return json.dumps(driver.get_snapshot_info(snapshot_id))

@api.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/<string:result>')
def get_result(user_id, snapshot_id, result):
    return json.dumps(driver.get_result(snapshot_id, result_name=result))

def run_api_server(host, port, database_url):
    db_url = furl(database_url)
    db_name, *_ = db_url.path.segments
    global driver
    driver = drivers[db_url.scheme]
    driver.init_db(name=db_name, host=db_url.host, port=db_url.port,
                   username=db_url.username, password=db_url.password)
    api.run(host=host, port=port)