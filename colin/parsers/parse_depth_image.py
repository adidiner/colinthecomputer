import matplotlib.pyplot as plt
import numpy as np

def parse_depth_image(context, snapshot):
	image = snapshot.depth_image
	x = np.array(image.data)
	x = x.reshape(image.height, image.width)
	plt.imshow(x)
	plt.savefig(context.directory / 'depth_image.jpg')

parse_depth_image.field = 'depth_image'