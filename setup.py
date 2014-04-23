# -*- coding: utf-8 -*-

# Copyright 2014 flask-mongoalchemy authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""
Flask MongoAlchemy
------------------

Adds Flask support for MongoDB using Mongo-Alchemy.

Links
`````

* `documentation <http://packages.python.org/Flask-MongoAlchemy>`_
* `development version
<http://github.com/cobrateam/flask-mongoalchemy/zipball/master#egg=Flask-MongoAlchemy-dev>`_

"""
from setuptools import setup

readme = __doc__
with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    name='Flask-MongoAlchemy',
    version='0.6.1',
    url='http://github.com/cobrateam/flask-mongoalchemy',
    license='BSD',
    author='Francisco Souza',
    author_email='francisco@franciscosouza.net',
    description='Add Flask support for MongoDB using MongoAlchemy.',
    long_description=readme,
    packages=['flask_mongoalchemy'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask>=0.9',
        'MongoAlchemy>=0.15',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
