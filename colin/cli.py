from inspect import getfullargspec
import sys

class CommandLineInterface:
	def __init__(self):
		# {name : (signature, function), ...}
		self.functions = {}

	def command(self, f):
		name = f.__name__
		sig = getfullargspec(f)
		self.functions[name] = (sig, f)
		return f

	def _create_dict(self, list):
		"""Creates dictionary from list = ['<key>=<value>'] (key, value non-empty),
		 returns None if invalid input."""
		if [s for s in list if s.count('=') != 1]:
			return None
		result = {}
		for item in list:
			key, value = item.split('=')
			if key == '' or value == '':
				return None
			result[key] = value
		return result

	def _valid_signature(self, sig, kwargs):
		"""Checks whether arguments in kwargs match signature arguments."""
		if kwargs is None:
			return False
		if sig.varkw is not None:
			return True
		return set(sig.args) == set(kwargs.keys())

	def main(self):
		usage_mes = f'USAGE: python {sys.argv[0]} <command> [<key>=<value>]*'
		if len(sys.argv) < 2:
			print(usage_mes)
			sys.exit(1)

		fname = sys.argv[1]
		if fname not in self.functions:
			print(usage_mes)
			sys.exit(1)

		sig, f = self.functions[fname]
		kwargs = self._create_dict(sys.argv[2:])
		if not self._valid_signature(sig, kwargs):
			print(usage_mes)
			sys.exit(1)

		f(**kwargs)
		sys.exit(0)



