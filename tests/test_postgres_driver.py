import pika
from multiprocessing import Process
import json
import pytest

from constants import USER, SNAPSHOTS, USER_JSON, SNAPSHOTS_JSON, POSE_JSON, COLOR_IMAGE_JSON, DEPTH_IMAGE_JSON, FEELINGS_JSON
import colinthecomputer.db_drivers as drivers
driver = drivers['postgresql']
# TODO: dont hard code host and port
_HOST = '127.0.0.1'
_PORT = 3333
_USERNAME = 'test'
_DB_NAME = 'test'
_PASSWORD = 'password'

# sudo docker run -d -e POSTGRES_PASSWORD=password -e POSTGRES_USER=test -p  3333:5432 postgres
# db://username:password@host:port/db_name
# postgresql://colin:password@127.0.0.1:3469/colin

@pytest.fixture
def init():
    driver.init_db(name=_DB_NAME, host=_HOST, port=_PORT,
                   username=_USERNAME, password=_PASSWORD)

@pytest.fixture
def fields():
    return ['pose', 'color_image', 'depth_image', 'feelings']


@pytest.fixture
def fields_data(fields):
    fields_data = {}
    jsons = [POSE_JSON, COLOR_IMAGE_JSON, DEPTH_IMAGE_JSON, FEELINGS_JSON]
    for field, data in zip(fields, jsons):
        fields_data[field] = json.loads(data[0])
    return fields_data


def test_save_get_user(init):
    user = json.loads(USER_JSON)
    driver.savers['user'](**user)
    print(driver.getters['users']())
    assert driver.getters['users']() == [{'user_id': user['user_id'],
                                        'username': user['username']}]
    print(driver.getters['user_info'](user['user_id']))
    assert driver.getters['user_info'](user['user_id']) == user


def test_save_get_snapshot(init, fields, fields_data):
    user = json.loads(USER_JSON)
    snapshot = json.loads(SNAPSHOTS_JSON[0])
    for field in fields:
        driver.savers[field](**fields_data[field])
    print(driver.getters['snapshots'](user['user_id']))
    assert len(driver.getters['snapshots'](user['user_id'])) == 1
    print(driver.getters['snapshot_info'](snapshot_id=1))
    assert driver.getters['snapshot_info'](snapshot_id=1) == \
           {'datetime': int(snapshot['datetime']), 'results': fields, 'snapshot_id': 1}
    for field in fields:
        print(driver.getters['result'](1, field))
        assert driver.getters['result'](1, field) == fields_data[field]['data']
    assert False
