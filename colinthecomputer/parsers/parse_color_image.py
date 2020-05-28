from colinthecomputer.utils import filtered_dict

from PIL import Image
from pathlib import Path
import json
import os

DIRECTORY = os.environ['BLOB_DIR'] + '/results' \
            if 'BLOB_DIR' in os.environ else 'colinfs/results'


def parse_color_image(data, directory=DIRECTORY):
    """
    Parse color image from snapshot data, save BLOB to fs.

    :param data: snapshot as consumed from the message queue
    :type data: json
    :returns: parsed snapshot color image,
              with a path to the parsed binary data
    :rtype: json
    """
    directory = Path(directory)
    data = json.loads(data)
    path = \
        directory / 'results' / str(data['user_id']) / data['datetime'] / 'color_image.jpg'
    # Create parsed metadata json
    color_image = _create_message(data, path)
    # Save parsed image to filesystem
    _save_binary(data, path)
    return json.dumps(color_image)


def _create_message(data, path):
    color_image = filtered_dict(data, ['user_id', 'datetime'])
    color_image['data'] = {'path': str(path)}
    return color_image


def _save_binary(data, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    data = data['color_image']
    with open(data['data'], 'rb') as file:
        result = Image.frombytes('RGB',
                                 (data['width'], data['height']),
                                 file.read())
    result.save(path)


parse_color_image.field = 'color_image'
