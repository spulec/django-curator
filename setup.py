#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='django-curator',
    version='0.1',
    author='Steve Pulec',
    author_email='spulec@gmail.com',
    url='http://github.com/spulec/django-curator',
    description = 'Automatic Business Graphs for Django',
    packages = find_packages(),
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)