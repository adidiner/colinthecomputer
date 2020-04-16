import pytest


from constants import USER, SNAPSHOTS, SNAPSHOTS_JSON, POSE_JSON, COLOR_IMAGE_JSON, DEPTH_IMAGE_JSON, FEELINGS_JSON
import mock_mq_driver as mq
from colinthecomputer.parsers import parsers
import numpy as np
from colinthecomputer.server.publisher import Publisher

@pytest.fixture
def blob_dir(tmp_path):
    """Directory containing the required binary data."""
    for snapshot in SNAPSHOTS:
        path = tmp_path / str(USER.user_id) / str(snapshot.datetime)
        if not path.exists():
            path.mkdir(parents=True)
        (path / 'color_image').write_bytes(snapshot.color_image.data)
        depth_image_data = np.array(snapshot.depth_image.data)
        np.save(str(path / 'depth_image'), depth_image_data)
    return tmp_path


def test_parse_pose():
   for snapshot, result in zip(SNAPSHOTS_JSON, POSE_JSON):
        assert parsers['pose'](snapshot) == result


def test_parse_color_image(blob_dir):
    for snapshot, result in zip(SNAPSHOTS_JSON, COLOR_IMAGE_JSON):
        snapshot = snapshot.replace('tmpdir', str(blob_dir))
        assert parsers['color_image'](snapshot, blob_dir) == result.replace('tmpdir', str(blob_dir))


def test_parse_depth_image(blob_dir):
    for snapshot, result in zip(SNAPSHOTS_JSON, DEPTH_IMAGE_JSON):
        snapshot = snapshot.replace('tmpdir', str(blob_dir))
        assert parsers['depth_image'](snapshot, blob_dir) == result.replace('tmpdir', str(blob_dir))


def test_feelings():
    for snapshot, result in zip(SNAPSHOTS_JSON, FEELINGS_JSON):
        assert parsers['feelings'](snapshot) == result