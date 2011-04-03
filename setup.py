#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

tests_require = [
    'django',
    'south',
]

setup(
    name='django-curator',
    version='0.1',
    author='Steve Pulec',
    author_email='spulec@gmail.com',
    url='http://github.com/spulec/django-curator',
    description = 'Automatic Business Graphs for Django',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)