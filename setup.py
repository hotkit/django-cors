#!/usr/bin/env python

from setuptools import setup

setup(
    name='django-cors',
    version='0.1.4',
    description='Classes for helping with CORS request to a Django service',
    author='Proteus Technologies Co. Ltd.',
    author_email='team@proteus-tech.com',
    url='https://github.com/Proteus-tech/django-cors',
    packages=['django_cors'],
    install_requires = ['Django>=1.3.1',],
)
