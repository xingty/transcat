# from distutils.core import setup, find_packages
from setuptools import setup,find_packages

VERSION = '0.0.3'

requirements = [
  'flask',
  'waitress',
  'requests',
  'langdetect',
]

setup(
  name='transcat',
  version=VERSION,
  description='A tool for managing translation services',
  author='Bigbyto',
  author_email='bigbyto@gmail.com',
  url='https://github.com/xingty/transcat',
  install_requires=requirements,
  python_requires='>=3.7',
  packages=find_packages(),
  entry_points={
    'console_scripts': [
      'transcat = src.cli:main',
    ]
  },
  data_files=[
    ('assets',['assets/schema.sql','assets/logging.conf']),
  ]

)