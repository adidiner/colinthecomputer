from PIL import Image as PImage

def parse_color_image(context, snapshot):
    image = snapshot.color_image
    image = PImage.frombytes('RGB', (image.width, image.height), image.data)
    image.save(context.directory / 'color_image.jpg')

parse_color_image.field = 'color_image'