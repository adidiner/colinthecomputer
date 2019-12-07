import json
from PIL import Image as PImage

parsers = {}


def parser(name):
    def decorator(f):
        parsers[name] = f
        return f
    return decorator


@parser('translation')
def parse_translation(context, snapshot):
    translation = {key: value for key, value in
                   zip(['x', 'y', 'z'], snapshot.translation)}
    with open(context.directory / 'translation.json', 'w') as writer:
        json.dump(translation, writer)


@parser('color_image')
def parse_color_image(context, snapshot):
    image = snapshot.color_image
    image = PImage.frombytes('RGB', (image.width, image.height), image.data)
    image.save(context.directory / 'color_image.jpg')
