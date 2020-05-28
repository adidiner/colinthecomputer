import pytest
from click.testing import CliRunner
import numpy as np
import pathlib

from constants import (USER,
                       SNAPSHOTS,
                       SNAPSHOTS_JSON,
                       POSE_JSON,
                       COLOR_IMAGE_JSON,
                       DEPTH_IMAGE_JSON,
                       FEELINGS_JSON
                       )
from colinthecomputer.parsers import parsers
from colinthecomputer.parsers.__main__ import cli_parse


@pytest.fixture
def blob_dir(tmp_path):
    """Directory containing the required binary data."""
    for snapshot in SNAPSHOTS:
        path = tmp_path / 'raw_data' / str(USER.user_id) / str(snapshot.datetime)
        path.mkdir(parents=True, exist_ok=True)
        (path / 'color_image').write_bytes(snapshot.color_image.data)
        depth_image_data = np.array(snapshot.depth_image.data)
        np.save(str(path / 'depth_image.npy'), depth_image_data)
    return tmp_path


def test_parse_pose():
    for snapshot, result in zip(SNAPSHOTS_JSON, POSE_JSON):
        assert parsers['pose'](snapshot) == result


def test_parse_color_image(blob_dir):
    for snapshot, result in zip(SNAPSHOTS_JSON, COLOR_IMAGE_JSON):
        snapshot = snapshot.replace('tmpdir', str(blob_dir))
        print(snapshot)
        assert parsers['color_image'](snapshot, blob_dir) == \
            result.replace('tmpdir', str(blob_dir))


def test_parse_depth_image(blob_dir):
    for snapshot, result in zip(SNAPSHOTS_JSON, DEPTH_IMAGE_JSON):
        snapshot = snapshot.replace('tmpdir', str(blob_dir))
        assert parsers['depth_image'](snapshot, blob_dir) == \
            result.replace('tmpdir', str(blob_dir))


def test_feelings():
    for snapshot, result in zip(SNAPSHOTS_JSON, FEELINGS_JSON):
        assert parsers['feelings'](snapshot) == result


def test_cli_parse(tmp_path):
    file = tmp_path / 'data.txt'
    file.write_text(SNAPSHOTS_JSON[0])
    runner = CliRunner()
    result = runner.invoke(cli_parse, ['pose', str(file)])
    assert result.exit_code == 0
    assert result.output == f'{POSE_JSON[0]}\n'
