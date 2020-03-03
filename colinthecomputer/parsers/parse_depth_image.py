import matplotlib.pyplot as plt
import numpy as np
import json
from pathlib import Path

directory = Path('/home/user/colinfs/results') # TODO

def parse_depth_image(data):
    data = json.loads(data)
    # Create parsed metadata json
    metadata = {}
    depth_image = data['depthImage']
    metadata['userID'], metadata['datetime'] = data['userID'], data['datetime']
    path = Path(depth_image['path'].replace('raw_data', 'results')).parent # TODO: temp sol
    if not path.exists():
         path.mkdir(parents=True)
    path /= 'depth_image.jpg'
    metadata['path'] = str(path)

    # Save parsed image to filesystem
    raw_data = np.load(depth_image['path'])
    raw_data = raw_data.reshape(depth_image['height'], depth_image['width'])
    plt.imshow(raw_data)
    plt.savefig(path)
    print(metadata)
    return json.dumps(metadata)


parse_depth_image.field = 'depth_image'