.. Flask MongoAlchemy documentation master file, created by
   sphinx-quickstart on Sat Nov 20 17:56:16 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Flask MongoAlchemy's documentation!
==============================================

.. module:: flaskext.mongoalchemy

Flask-MongoAlchemy adds support for `MongoDB`_ on `Flask`_ using `MongoAlchemy`_. Source code and issue tracking at `Github`_.

Installation
------------

You can easily install using *pip* or *easy_install*:

::

    $ [sudo] pip install Flask-MongoAlchemy
    $ [sudo] easy_install Flask-MongoAlchemy

If you prefer, you can use the last source version by cloning git repository:

::

    $ git clone https://github.com/franciscosouza/flask-mongoalchemy.git
    $ cd flask-mongoalchemy
    $ [sudo] python setup.py develop

Make sure you have MongoDB installed for use it.

Configuration values
--------------------

The following configuration values exist for Flask-MongoAlchemy:

.. tabularcolumns:: |p{6.5cm}|p{8.5cm}|

=============================== =========================================
``MONGOALCHEMY_DATABASE``       The database name that should be used for
                                the connection.
``MONGOALCHEMY_SERVER``         The MongoDB server.

                                *Default value:* ``localhost``
``MONGOALCHEMU_PORT``           Port where MongoDB server is listening.

                                *Default value:* ``27017``
``MONGOALCHEMY_USER``           User for database connection.

                                *Default value:* ``None``
``MONGOALCHEMY_PASSWORD``       Password for database connection.

                                *Default value:* ``None``
=============================== =========================================

API
---

This part of the documentation documents all the public classes and
functions in Flask-MongoAlchemy.

Configuration
+++++++++++++

.. autoclass:: MongoAlchemy
   :members:

Documents
+++++++++

.. autoclass:: Document
   :members:

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _Flask: http://flask.pocoo.org
.. _Github: http://github.com/franciscosouza/flask-mongoalchemy
.. _MongoDB: http://mongodb.org
.. _MongoAlchemy: http://mongoalchemy.org
