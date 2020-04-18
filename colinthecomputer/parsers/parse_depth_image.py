import matplotlib.pyplot as plt
import numpy as np
import json
import os
from pathlib import Path

from colinthecomputer.utils import filtered_dict


def parse_depth_image(data, directory=os.environ['BLOB_DIR'] + '/results'):
    """Parse depth image from snapshot data, save BLOB to fs.
    
    :param data: snapshot as consumed from the message queue
    :type data: json
    :returns: parsed snapshot depth image, with a path to the parsed binary data
    :rtype: json
    """
    directory = Path(directory)
    data = json.loads(data)
    # Create parsed metadata json
    depth_image = filtered_dict(data, ['user_id', 'datetime'])
    path = directory / str(depth_image['user_id']) / depth_image['datetime']
    if not path.exists():
         path.mkdir(parents=True)
    path /= 'depth_image.jpg'
    depth_image['data'] = {'path': str(path)}

    # Save parsed image to filesystem
    data = data['depth_image']
    blob = np.load(data['data'])
    blob = blob.reshape(data['height'], data['width'])
    plt.imshow(blob)
    plt.savefig(path)
    return json.dumps(depth_image)


parse_depth_image.field = 'depth_image'