import datetime as dt
import pytest

from colin.utils import Reader


_SAMPLE = '/home/user/sample.mind' #TODO: upload sample to git??
_USER_ID = 42
_USERNAME = 'Dan Gittik'
_BIRTH_DATE = dt.datetime(1992, 3, 5)
_GENDER = 'm'

@pytest.fixture
def reader():
    reader = Reader(_SAMPLE)
    yield reader


def test_user_info(reader):
	assert reader.user_id == _USER_ID
	assert reader.username == _USERNAME
	assert reader.birth_date == _BIRTH_DATE
	assert reader.gender == _GENDER
