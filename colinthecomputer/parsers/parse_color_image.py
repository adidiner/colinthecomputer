from colinthecomputer.utils import make_path

from PIL import Image
from pathlib import Path
import json

directory = Path('/home/user/colinfs/results') # TODO

def parse_color_image(data):
    data = json.loads(data)
    # Create parsed metadata json
    metadata = {}
    color_image = data['color_image']
    metadata['user_id'], metadata['datetime'] = data['user_id'], data['datetime']
    path = Path(color_image['path'].replace('raw_data', 'results')).parent # TODO: temp sol
    if not path.exists():
         path.mkdir(parents=True)
    path /= 'color_image.jpg'
    metadata['data'] = {}
    metadata['data']['path'] = str(path)

    # Save parsed image to filesystem
    with open(color_image['path'], 'rb') as file:
        result = Image.frombytes('RGB', (color_image['width'], color_image['height']), file.read()) 
    result.save(path)
    print(metadata)
    return json.dumps(metadata)

parse_color_image.field = 'color_image'