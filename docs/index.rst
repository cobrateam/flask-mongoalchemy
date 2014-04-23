.. Flask MongoAlchemy documentation master file, created by
   sphinx-quickstart on Sat Nov 20 17:56:16 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Flask MongoAlchemy's documentation!
==============================================

.. module:: flask.ext.mongoalchemy

Flask-MongoAlchemy adds support for `MongoDB`_ on `Flask`_ using `MongoAlchemy`_. Source code and issue tracking are available at `Github`_. If you want to get started, check out the `example source code <http://github.com/cobrateam/flask-mongoalchemy/tree/master/examples>`_.

Installation
------------

You can easily install using `pip` or `easy_install`:

::

    $ [sudo] pip install Flask-MongoAlchemy
    $ [sudo] easy_install Flask-MongoAlchemy

If you prefer, you may use the latest source version by cloning the following git repository:

::

    $ git clone https://github.com/cobrateam/flask-mongoalchemy.git
    $ cd flask-mongoalchemy
    $ [sudo] python setup.py develop

Make sure you have MongoDB installed to use it.

Usage
-----

It is very easy and fun to use Flask-MongoAlchemy to proxy between Python and MongoDB.

All you have to do is create a MongoAlchemy object and use it to declare documents. Here is a complete example:

::

    from flask import Flask
    from flask.ext.mongoalchemy import MongoAlchemy
    app = Flask(__name__)
    app.config['MONGOALCHEMY_DATABASE'] = 'library'
    db = MongoAlchemy(app)

    class Author(db.Document):
        name = db.StringField()

    class Book(db.Document):
        title = db.StringField()
        author = db.DocumentField(Author)
        year = db.IntField()

As you can see, extending the :class:`Document` is all you need to create a document.

Now you can create authors and books:

::

    >>> from application import Author, Book
    >>> mark_pilgrim = Author(name='Mark Pilgrim')
    >>> dive = Book(title='Dive Into Python', author=mark_pilgrim, year=2004)

And save them:

::

    >>> mark_pilgrim.save()
    >>> dive.save()

If you make any changes on a document, you may call :meth:`~Document.save` again:

::

    >>> mark_pilgrim.name = 'Mark Stalone'
    >>> mark_pilgrim.save()

And you can remove a document from the database by calling its :meth:`~Document.remove` method:

::

    >>> dive.remove()

Another basic operation is querying for documents. Every document has a ``query`` class property. It's very simple to use it:

::

    >>> mark = Author.query.get('76726')
    >>> mark.name = 'Mark Pilgrim'
    >>> mark.save()

You also can use the ``filter`` method instead of the :meth:`~BaseQuery.get` method:

::

    >>> mark = Author.query.filter(Author.name == 'Mark Pilgrim').first()
    >>> mark.name = 'Steve Jobs'
    >>> mark.save()

Do you want to go further? Dive deep into the `API`_ docs.

Using authenticated connections
-------------------------------

It's possible to use authentication to connect to a MongoDB server. The authentication can be server based or database based.

The default behavior is to use server based authentication, to use database based authentication, you need to turn off the config
value ``MONGOALCHEMY_SERVER_AUTH`` (see the next section for more detail on configuration values):

::

    >>> app.config['MONGOALCHEMY_SERVER_AUTH'] = False

Configuration values
--------------------

The following configuration values are present in Flask-MongoAlchemy:

.. tabularcolumns:: |p{6.5cm}|p{8.5cm}|

=============================== =========================================
``MONGOALCHEMY_DATABASE``       The database name that should be used for
                                the connection.
``MONGOALCHEMY_SERVER``         The MongoDB server.

                                *Default value:* ``localhost``

``MONGOALCHEMY_PORT``           Listening port of the MongoDB server.

                                *Default value:* ``27017``

``MONGOALCHEMY_USER``           User for database connection.

                                *Default value:* ``None``

``MONGOALCHEMY_PASSWORD``       Password for database connection.

                                *Default value:* ``None``

``MONGOALCHEMY_SAFE_SESSION``   Use session in safe mode. When in safe
                                mode, all methods like ``save`` and
                                ``delete`` wait for the operation to
                                complete.

                                *Default value:* ``False``

 ``MONGOALCHEMY_OPTIONS``       Pass extra options to the MongoDB server
                                when connecting.

                                *e.g.:* safe=true
                                *Default value:* ``None``

 ``MONGOALCHEMY_SERVER_AUTH``   Boolean value indicating to use server based
                                authentication or not. When ``False``, will use
                                database based authentication.

                                *Default value:* ``True``

 ``MONGOALCHEMY_REPLICA_SET``   Name of the replica set to be used. Empty for
                                no replica sets.

                                *Default value:* ````

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

Querying
++++++++

.. autoclass:: BaseQuery
   :members:

Utilities
+++++++++

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
