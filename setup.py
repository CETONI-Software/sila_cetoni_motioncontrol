from os.path import dirname, join

from setuptools import setup

setup(
    long_description=open(join(dirname(__file__), "README.md")).read(),
)
