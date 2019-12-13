import datetime as dt
import pytest

from colin.utils import Reader
from colin.utils.snapshot import Snapshot, Image


_SAMPLE = 'test_sample.mind'
_USER_ID = 49
_USERNAME = 'Adi Dinerstein'
_BIRTH_DATE = dt.datetime.fromtimestamp(974239200)
_GENDER = 'f'
_COLOR_IMAGE = Image('color', 10, 20, b'0'*20*10*3)
_DEPTH_IMAGE = Image('depth', 5, 7, b'0'*7*5*4)
_SNAPSHOT1 = Snapshot(1576237612000, (1.0, 2.0, 3.0),
                      (1.0, 2.0, 3.0, 4.0),
                      _COLOR_IMAGE, _DEPTH_IMAGE,
                      (-0.5, -0.125, -0.5, 0.5))
_SNAPSHOT2 = Snapshot(1576237618000, (0.5, 3.0, 4.0),
                      (3.0, 3.0, 3.0, 3.0),
                      _COLOR_IMAGE, _DEPTH_IMAGE,
                      (0.5, 0.125, 1.0, -0.5))
_SNAPSHOTS = [_SNAPSHOT1, _SNAPSHOT2]


@pytest.fixture
def reader():
    reader = Reader(_SAMPLE)
    yield reader


def test_user_info(reader):
    assert reader.user_id == _USER_ID
    assert reader.username == _USERNAME
    assert reader.birth_date == _BIRTH_DATE
    assert reader.gender == _GENDER


def test_read_snapshots(reader):
    iterations = 0
    for snapshot in reader:
        assert snapshot == _SNAPSHOTS[iterations]
        iterations += 1
    assert iterations == len(_SNAPSHOTS)
