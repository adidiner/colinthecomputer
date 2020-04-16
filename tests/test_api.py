from colinthecomputer.api.api import app
import mock_mq_driver

def mock_driver(monkeypatch):
	monkeypatch.setattr(colinthecomputer, 'db_drivers', {'url': mock_mq_driver})


def test_get_users():
	pass