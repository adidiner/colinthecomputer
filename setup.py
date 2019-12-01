from setuptools import setup, find_packages


setup(
    name = 'colin-the-computer',
    version = '0.0.1',
    author = 'Adi Dinerstein',
    description = 'Project for Advanced System Design course, TAU.',
    packages = find_packages(),
    install_requires = ['click', 'flask'],
    tests_require = ['pytest'],
)