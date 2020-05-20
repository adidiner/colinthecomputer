from setuptools import setup, find_packages


setup(
    name = 'colin-the-computer',
    version = '0.1.0',
    author = 'Adi Dinerstein',
    description = 'Project for Advanced System Design course, TAU.',
    packages = find_packages(),
    install_requires = ['click',
                        'flask',
                        'Flask-Cors'
                        'furl',
                        'matplotlib',
                        'numpy',
                        'peewee',
                        'pika',
                        'protobuf',
                        'Pillow',
                        'psycopg2',
                        'requests',
                        'Werkzeug',
    ]
    tests_require = ['pytest'
                     'codecov',
    ],
)