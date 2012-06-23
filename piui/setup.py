from setuptools import setup, find_packages

setup(
   name = 'piui',
   version = '0.1',
   packages = find_packages(),
   
   author = 'Russell Hay',
   author_email = 'me@russellhay.com',
   description = 'UI required by PhotoClog',
   url = 'https://github.com/Trepython/PhotoClog',

   setup_requires=['nose'],
   tests_require=['coverage'],
)
