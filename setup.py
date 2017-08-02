
from setuptools import setup, find_packages

setup(
    name='usql',
    version='0.0.5',
    description='A quicker way to write SQL',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    url='https://github.com/ivankocienski/usql',
    author='Ivan Kocienski',
    author_email='ivan [dot] kocienski [at] gmail [dot] com',
    license='BSD')
