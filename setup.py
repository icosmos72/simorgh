import os
from setuptools import setup


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


VERSION = "0.0.1"

setup(
    name="simorgh",
    version=VERSION,
    author="Matthew Wampler-Doty",
    description=("A database for collecting and serving data from the TESS Dragon test bench"),
    license="GPL3",
    keywords="database",
    url="https://github.com/TESScience/simorgh",
    packages=['mcc'],
    download_url='https://github.com/TESScience/simorgh/tarball/{VERSION}'.format(VERSION=VERSION),
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 2.7",
        "Topic :: Database",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    scripts=['temperature_monitor'],
    requires=['cherrypy']
)
