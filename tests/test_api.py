import colinthecomputer.api.api as api
from colinthecomputer.api.api import app
import mock_db_driver
import pytest


@pytest.fixture
def blob_results(tmp_path):
    (tmp_path / 'color_image.jpg').write_bytes(b'000')
    (tmp_path / 'depth_image.jpg').write_bytes(b'000')
    mock_db_driver.tmpdir = str(tmp_path)
    return tmp_path


@pytest.fixture
def mock_getters(monkeypatch):
    monkeypatch.setattr(api, 'getters', mock_db_driver.getters)


def test_get_users(mock_getters):
    with app.test_client() as c:
        resp = c.get('/users')
        assert resp.get_json() == 'users'


def test_get_info(mock_getters):
    with app.test_client() as c:
        resp = c.get('/users/67')
        assert resp.get_json() == {'67': 'user_info'}
        resp = c.get('/users/0')
        assert resp.get_json() == {'0': 'user_info'}
        resp = c.get('users/a')
        assert resp.status_code == 404


def test_get_snapshots(mock_getters):
    with app.test_client() as c:
        resp = c.get('/users/67/snapshots')
        assert resp.get_json() == {'67': 'snapshots'}
        resp = c.get('/users/0/snapshots')
        assert resp.get_json() == {'0': 'snapshots'}
        resp = c.get('users/a/snapshots')
        assert resp.status_code == 404


def test_get_snapshot_info(mock_getters):
    with app.test_client() as c:
        resp = c.get('/users/67/snapshots/55')
        assert resp.get_json() == {'55': 'snapshot_info'}
        resp = c.get('/users/0/snapshots/0')
        assert resp.get_json() == {'0': 'snapshot_info'}
        resp = c.get('users/67/snapshots/bb')
        assert resp.status_code == 404


def test_get_result(blob_results, mock_getters):
    with app.test_client() as c:
        resp = c.get('/users/67/snapshots/55/pose')
        assert resp.get_json() == {'result': 'pose'}
        resp = c.get('/users/67/snapshots/55/color_image')
        assert resp.get_json() == {'path': '/users/67/snapshots/55/color_image/data.jpg'}
        resp = c.get('/users/67/snapshots/55/depth_image')
        assert resp.get_json() == {'path': '/users/67/snapshots/55/depth_image/data.jpg'}
        resp = c.get('/users/67/snapshots/55/feelings')
        assert resp.get_json() == {'result': 'feelings'}
        resp = c.get('/users/67/snapshots/55/roy')
        assert resp.status_code == 404


def test_get_blob_data(blob_results, mock_getters):
     with app.test_client() as c:
        resp = c.get('/users/67/snapshots/55/pose/data.jpg')
        assert resp.status_code == 404
        resp = c.get('/users/67/snapshots/55/color_image/data.jpg')
        assert resp.get_data() == b'000'
        resp = c.get('/users/67/snapshots/55/depth_image/data.jpg')
        assert resp.get_data() == b'000'
        resp = c.get('/users/67/snapshots/55/feelings/data.jpg')
        assert resp.status_code == 404
