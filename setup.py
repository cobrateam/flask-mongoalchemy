"""
Flask MongoAlchemy
------------------

Adds Flask support for MongoDB using Mongo-Alchemy.

Links
`````

* `documentation <http://packages.python.org/Flask-MongoAlchemy>`_
* `development version
  <http://github.com/franciscosouza/flask-mongoalchemy/zipball/master#egg=Flask-MongoAlchemy-dev>`_

"""
from setuptools import setup

readme = __doc__
with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    name='Flask-MongoAlchemy',
    version='0.1',
    url='http://github.com/cobrateam/flask-mongoalchemy',
    license='BSD',
    author='Francisco Souza',
    author_email='francisco@franciscosouza.net',
    description='Add Flask support for MongoDB using MongoAlchemy.',
    long_description=readme,
    packages=['flaskext'],
    namespace_packages=['flaskext'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
        'MongoAlchemy',
        'pymongo',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
