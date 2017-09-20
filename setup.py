#!/usr/bin/env python

import os
import re
import sys

from codecs import open

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


packages = [
    'ssshelf',
    'ssshelf.storages'
]


requires = [
    "aiobotocore>=0.4.5",
    "paco>=0.1.11",
    "retrying>=1.3.3",
    "pygtrie>=2.2",
    "six>=1.10.0",
]

test_requirements = [
    "moto",
    "pytest",
    "requests",
    "flask",
    "attrs",
    "iso8601==0.1.12",
    "pytest-asyncio",
    "pystrainer==1.3.1",
    "simpleflake",
]

with open('ssshelf/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()


setup(
    name='ssshelf',
    version=version,
    description='A collection and persistance manager for blob stores like aws S3',
    long_description=readme,
    author='Alex Kessinger',
    author_email='voidfiles@gmail.com',
    url='http://github.com/voidfiles/ssshelf',
    packages=packages,
    package_data={
        '': [
            'LICENSE',
            '*.txt',
        ],
        'ssshelf': []
    },
    package_dir={
        'ssshelf': 'ssshelf',
    },
    include_package_data=True,
    install_requires=requires,
    license='Apache 2.0',
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Development Status :: 5 - Production/Stable',
        'Topic :: Software Development',
    ],
    cmdclass={'test': PyTest},
    tests_require=test_requirements,
)
