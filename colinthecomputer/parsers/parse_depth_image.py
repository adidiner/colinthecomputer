import matplotlib.pyplot as plt
import numpy as np
import json
import os
from pathlib import Path

from colinthecomputer.utils import filtered_dict

DIRECTORY = os.environ['BLOB_DIR'] \
            if 'BLOB_DIR' in os.environ else 'colinfs'


def parse_depth_image(data, directory=DIRECTORY):
    """
    Parse depth image from snapshot data, save BLOB to fs.

    :param data: snapshot as consumed from the message queue
    :type data: json
    :returns: parsed snapshot depth image,
              with a path to the parsed binary data
    :rtype: json
    """
    directory = Path(directory)
    data = json.loads(data)
    path = \
        directory / 'results' / str(data['user_id']) / data['datetime'] / 'depth_image.jpg'
    # Create parsed metadata json
    depth_image = _create_message(data, path)
    # Save parsed image to filesystem
    _save_binary(data, path)
    return json.dumps(depth_image)


def _create_message(data, path):
    depth_image = filtered_dict(data, ['user_id', 'datetime'])
    depth_image['data'] = {'path': str(path)}
    return depth_image


def _save_binary(data, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    data = data['depth_image']
    blob = np.load(data['data'])
    blob = blob.reshape(data['height'], data['width'])
    plt.imshow(blob)
    plt.savefig(path)


parse_depth_image.field = 'depth_image'
