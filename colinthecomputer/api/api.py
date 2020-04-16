from flask import Flask
from flask import send_file
from flask import abort
from flask import jsonify
from flask_cors import CORS
from furl import furl
import io

import colinthecomputer.db_drivers as drivers
getters = None


app = Flask(__name__)
CORS(app)

@app.route('/users')
def get_users():
    """GET all available users.
    
    :returns: users json, in the form [{"user_id":id, "username":name}, ...]
    :rtype: json
    """
    return jsonify(getters['users']())

@app.route('/users/<int:user_id>')
def get_user_info(user_id):
    """GET the given user's information.
    
    :param user_id: user id of the requested user
    :type user_id: int
    :returns: user info json, in the form 
    {"birthday":sec from epoch,"gender":"m"/"f"/"o","user_id":id,"username":name}
    :rtype: json
    """
    result = getters['user_info'](user_id)
    if not result:
        abort(404)
    return jsonify(result)

@app.route('/users/<int:user_id>/snapshots')
def get_snapshots(user_id):
    """GET the user's available snapshots.
    
    :param user_id: user id of the requested user
    :type user_id: int
    :returns: snapshots json, in the form
    [{"datetime":milisec from epoch,"snapshot_id":id}, ...]
    :rtype: json
    """
    return jsonify(getters['snapshots'](user_id))

@app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>')
def get_snapshot_info(user_id, snapshot_id):
    """GET the snapshot's information.
    
    :param user_id: user corresponding to snapshot
    :type user_id: int
    :param snapshot_id: the given snapshot's id
    :type snapshot_id: int
    :returns: snapshot info json, in the form
    {"datetime":milisec frm epoch,"results":[available results],"snapshot_id":id}
    :rtype: json
    """
    result = getters['snapshot_info'](snapshot_id)
    if not result:
        abort(404)
    return jsonify(result)

@app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/<string:result_name>')
def get_result(user_id, snapshot_id, result_name):
    """GET result json, only  if available. 
    
    :param user_id: user corresponding to snapshot
    :type user_id: int
    :param snapshot_id: snapshot corresponding to result
    :type snapshot_id: int
    :param result_name: required result, one of 
    pose, color_image, depth_image, feelings
    :type result_name: str
    :returns: json describing the result
    for BLOBS, the json contains path to the binary data
    :rtype: json
    """
    result = getters['result'](snapshot_id, result_name=result_name)
    if not result:
        abort(404)
    blobs = ['color_image', 'depth_image']
    if result_name not in blobs:
        return jsonify(result)
    return {'path': f'/users/{user_id}/snapshots/{snapshot_id}/{result_name}/data.jpg'}

@app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/<string:result_name>/data.jpg')
def get_blob_data(user_id, snapshot_id, result_name):
    """GET blob data of a result (can be viewd in the browser).
    
    :param user_id: user corresponding to snapshot
    :type user_id: int
    :param snapshot_id: snapshot corresponding to result
    :type snapshot_id: int
    :param result_name: required result, one of color_image, depth_image
    :type result_name: str
    :returns: the image
    :rtype: jpg
    """
    blobs = ['color_image', 'depth_image']
    result = getters['result'](snapshot_id, result_name=result_name)
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
        global getters
        driver = drivers[db_url.scheme]
        getters = driver.getters
        driver.init_db(name=db_name, host=db_url.host, port=db_url.port,
                       username=db_url.username, password=db_url.password)
        app.run(host=host, port=port)
    except Exception as error:
        print(f"ERROR in {__name__}: {error}")