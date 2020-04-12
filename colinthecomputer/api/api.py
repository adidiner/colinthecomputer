from flask import Flask
from flask import send_file
from flask import abort
from flask import jsonify
from flask_cors import CORS
from furl import furl
import io


from colinthecomputer.db_drivers import postgresql_driver

drivers = {'postgresql': postgresql_driver}
driver = None

api = Flask(__name__)
CORS(api)

@api.route('/users')
def get_users():
    return jsonify(driver.get_users())

@api.route('/users/<int:user_id>')
def get_user_info(user_id):
    result = driver.get_user_info(user_id)
    if not result:
        abort(404)
    return jsonify(result)

@api.route('/users/<int:user_id>/snapshots')
def get_snapshots(user_id):
    return jsonify(driver.get_snapshots(user_id))

@api.route('/users/<int:user_id>/snapshots/<int:snapshot_id>')
def get_snapshot_info(user_id, snapshot_id):
    result = driver.get_snapshot_info(snapshot_id)
    if not result:
        abort(404)
    return jsonify(result)

@api.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/<string:result_name>')
def get_result(user_id, snapshot_id, result_name):
    result = driver.get_result(snapshot_id, result_name=result_name)
    if not result:
        abort(404)
    blobs = ['color_image', 'depth_image']
    if result_name not in blobs:
        return jsonify(result)
    return {'path': f'/users/{user_id}/snapshots/{snapshot_id}/{result_name}/data.jpg'}

@api.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/<string:result_name>/data.jpg')
def get_blob_data(user_id, snapshot_id, result_name):
    blobs = ['color_image', 'depth_image']
    result = driver.get_result(snapshot_id, result_name=result_name)
    if result_name not in blobs or not result:
        abort(404)
    path = result['path']
    return send_file(path,
                     attachment_filename=f'{result_name}.jpg',
                     mimetype='image/jpg')

def run_api_server(host, port, database_url):
    """Run the API server on (host, port), quering the given db.
    
    :param host: API ip address
    :type host: str
    :param port: API port
    :type port: int
    :param database_url: specifies the database to serve from,
    in the form db://username:password@host:port/db_name
    :type database_url: str
    """
    try:
        db_url = furl(database_url)
        db_name, *_ = db_url.path.segments
        global driver
        driver = drivers[db_url.scheme]
        driver.init_db(name=db_name, host=db_url.host, port=db_url.port,
                       username=db_url.username, password=db_url.password)
        api.run(host=host, port=port)
    except Exception as error:
        print(f"ERROR in {__name__}: {error}")