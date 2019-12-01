import datetime as dt
import struct

import pytest

from colin import Thought


user_id = 1
datetime = dt.datetime(2000, 1, 1, 12, 0)
thought = "I'm hungry"
serialized = b"\x01\x00\x00\x00\x00\x00\x00\x00 \xd0m8\x00\x00\x00\x00\n\x00\x00\x00I'm hungry"


@pytest.fixture
def t():
    return Thought(user_id, datetime, thought)


def test_attributes(t):
    assert t.user_id == user_id
    assert t.timestamp == datetime
    assert t.thought == thought


def test_repr(t):
    assert repr(t) == f'Thought(user_id={user_id!r}, timestamp={datetime!r}, thought={thought!r})'


def test_str(t):
    assert str(t) == f'[{datetime:%Y-%m-%d %H:%M:%S}] user {user_id}: {thought}'


def test_eq(t):
    t1 = Thought(user_id, datetime, thought)
    assert t1 == t
    t2 = Thought(user_id + 1, datetime, thought)
    assert t2 != t
    t3 = Thought(user_id, datetime + dt.timedelta(minutes=1), thought)
    assert t3 != t
    t4 = Thought(user_id, datetime, thought + '!')
    assert t4 != t
    t5 = 1
    assert t5 != t
    t6 = lambda: None
    t6.user_id = user_id
    t6.timestamp = datetime
    t6.thought = thought
    assert t6 != t


def test_serialize(t):
    assert t.serialize() == serialized


def test_deserialize(t):
    t = Thought.deserialize(serialized)
    assert t.user_id == user_id
    assert t.timestamp == datetime
    assert t.thought == thought


def test_symmetry(t):
    assert Thought.deserialize(t.serialize()) == t
