# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


long_description = open('README.md').read()


setup(
    name='django-timelinejs',
    version='0.0.1',
    description='A Django app for feeding data into a TimelineJS presentation',
    long_description=long_description,
    author='Ryan Pitts',
    author_email='ryan.a.pitts@gmail.com',
    url='https://github.com/iris-edu/django-timelinejs',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    zip_safe=False,
    install_requires=[],
)

