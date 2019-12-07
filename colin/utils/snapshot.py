class Image:
	def __init__(self, im_type, width, height, data):
		self.type = im_type
		self.width = width
		self.height = height
		self.data = data

	def __repr__(self):
		return f'<Image: {self.type} {self.width}x{self.height}>'


class Snapshot:
	def __init__(self, datetime):
		self.datetime = datetime
		self.translation = (0, 0, 0)
		self.rotation = (0, 0, 0, 0)
		self.color_image = Image('color', 0, 0, None)
		self.depth_image = Image('depth', 0, 0, None)
		self.feelings = (0, 0, 0, 0)