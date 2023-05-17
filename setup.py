# from distutils.core import setup, find_packages
from setuptools import setup,find_packages

requirements = [
  'flask',
  'requests',
  'langdetect'
]

setup(
  name='transcat',
  version='0.0.1',
  description='A tool for managing translation services',
  author='Bigbyto',
  author_email='bigbyto@gmail.com',
  url='https://github.com/bigbyto/transcat',
  require_packages=requirements,
  packages=find_packages(),
  data_files=[
    ('assets',['assets/schema.sql','assets/logging.conf']),
  ],

)