import os
from setuptools import setup, find_packages
from glob import glob


def read(file_name):
    """Read the contents of a file to a string"""
    with open(os.path.join(os.path.dirname(__file__), file_name)) as f:
        return f.read()


NAME = 'simorgh'
VERSION = "0.0.1"

setup(
    name=NAME,
    version=VERSION,
    author="Matthew Wampler-Doty",
    description="A database for collecting and serving data from the TESS Dragon test bench",
    license="GPL3",
    keywords="database",
    url="https://github.com/TESScience/${NAME}",
    packages=find_packages(),
    package_data={
        'simorgh': ['data/schemas/*.json']
    },
    long_description= read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 2.7",
        "Topic :: Database",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    scripts=glob('scripts/*'),
    install_requires=['cherrypy>=5.0.1', 'jsonschema>=2.5.1', 'tinydb>=3.1.3']
)
