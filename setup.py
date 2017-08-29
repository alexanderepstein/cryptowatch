#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os
import sys

from setuptools import find_packages, setup

# Package meta-data.
NAME = 'crypotowatch'
DESCRIPTION = 'Track prices and account balances for bitcoin, ethereum, and litecoin'
URL = 'https://github.com/alexanderepstein/cryptowatch'
EMAIL = 'epsteina@wit.edu'
AUTHOR = 'Alexander Epstein'

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

# Load the package's __version__.py module as a dictionary.
about = {}
with open(os.path.join(here, "__version__.py")) as f:
    exec(f.read(), about)

# Support "$ setup.py publish".
if sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel upload")
    sys.exit()

# What packages are required for this module to be executed?
required = [
     'requests', 'Adafruit_GPIO'
]

# Dependencies only for versions less than Python 2.7:
# if sys.version_info < (2, 7):
#     required.append('requests[security]')

# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    entry_points={
        'console_scripts': ['cryptowatch=cryptoConsole.cryptowatch:main'],
    },
    install_requires=required,
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
