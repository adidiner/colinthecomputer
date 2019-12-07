import pathlib
import json
from reader import Reader #!!
from PIL import Image as PImage

parsers = {}

def parser(name):
	def decorator(f):
		parsers[name] = f
		return f
	return decorator


@parser('translation')
def parse_translation(context, snapshot):
	translation = {key: value for key, value in \
				   zip(['x', 'y', 'z'], snapshot.translation)}
	with open(context.directory / 'translation.json', 'w') as writer:
		json.dump(translation, writer)


@parser('color_image')
def parse_color_image(context, snapshot):
	image = snapshot.color_image
	image = PImage.frombytes('RGB', (image.width, image.height), image.data)
	image.save(context.directory / 'color_image.jpg')

reader = Reader('/home/user/sample.mind')
data_dir = '/home/user/test/'
user_id = 42
for snapshot in reader:
	datetime = snapshot.datetime.strftime('%Y-%m-%d_%H-%M-%S-%f')
	path = pathlib.Path(data_dir) / f'{user_id}'
	if not path.exists():
		path.mkdir()
	path /= datetime
	if not path.exists():
		path.mkdir()
	context = Context(path)
	parsers['translation'](context, snapshot)
	parsers['color_image'](context, snapshot)
	break

