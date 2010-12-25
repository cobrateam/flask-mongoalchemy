.. Flask MongoAlchemy documentation master file, created by
   sphinx-quickstart on Sat Nov 20 17:56:16 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Flask MongoAlchemy's documentation!
==============================================

.. module:: flaskext.mongoalchemy

Flask-MongoAlchemy adds support for `MongoDB`_ on `Flask`_ using `MongoAlchemy`_. Source code and issue tracking at `Github`_. If you want to get started, check the `example sourcecode <http://github.com/cobrateam/flask-mongoalchemy/tree/master/examples>`_ out.

Installation
------------

You can easily install using *pip* or *easy_install*:

::

    $ [sudo] pip install Flask-MongoAlchemy
    $ [sudo] easy_install Flask-MongoAlchemy

If you prefer, you can use the last source version by cloning git repository:

::

    $ git clone https://github.com/cobrateam/flask-mongoalchemy.git
    $ cd flask-mongoalchemy
    $ [sudo] python setup.py develop

Make sure you have MongoDB installed for use it.

Usage
-----

It is very easy and fun to use Flask-MongoAlchemy to proxy between Python and MongoDB.

All you have to do is to create an MongoAlchemy object and use this to declare documents. Here a complete example:

::

    from flask import Flask
    from flaskext.mongoalchemy import MongoAlchemy
    app = Flask(__name__)
    app.config['MONGOALCHEMY_DATABASE'] = 'library'
    db = MongoAlchemy(app)

    class Author(db.Document):
        name = db.StringField()

    class Book(db.Document):
        title = db.StringField()
        author = db.DocumentField(Author)
        year = db.IntField()

As you can see, you just need to extend :class:`Document` to create a document.

Now you can create authors and books:

::

    >>> from application import Author, Book
    >>> mark_pilgrin = Author(name='Mark Pilgrin')
    >>> dive = Book(title='Dive Into Python', author=mark_pilgrin, year=2004)

And you can save them:

::

    >>> mark_pilgrin.save()
    >>> dive.save()

If you make any change on a document, you can call :meth:`~Document.save` again:

::

    >>> mark_pilgrin.name = 'Mark Pillgrin'
    >>> mark_pilgrin.save()

And you can remove a document from database by calling its :meth:`~Document.remove` method:

::

    >>> dive.remove()

Configuration values
--------------------

The following configuration values exist for Flask-MongoAlchemy:

.. tabularcolumns:: |p{6.5cm}|p{8.5cm}|

=============================== =========================================
``MONGOALCHEMY_DATABASE``       The database name that should be used for
                                the connection.
``MONGOALCHEMY_SERVER``         The MongoDB server.

                                *Default value:* ``localhost``
``MONGOALCHEMY_PORT``           Port where MongoDB server is listening.

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

Queries and pagination
++++++++++++++++++++++

.. autoclass:: BaseQuery
   :members:

.. autoclass:: Pagination
   :members:

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _Flask: http://flask.pocoo.org
.. _Github: http://github.com/cobrateam/flask-mongoalchemy
.. _MongoDB: http://mongodb.org
.. _MongoAlchemy: http://mongoalchemy.org
