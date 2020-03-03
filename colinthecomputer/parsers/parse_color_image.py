from PIL import Image
from pathlib import Path
import json


def parse_color_image(data):
    data = json.loads(data)
    image = data['colorImage']
    #image = PImage.frombytes('RGB', (image['width'], image['height'], image.data)
    with open(image['path'], 'rb') as file:
        bytestring = file.read()
        result = Image.frombuffer('RGB', (image['width'], image['height']), bytestring)
    result.save(Path('/home/user/test/color_image.jpg'))
    print('s')

parse_color_image.field = 'color_image'