Flask-MongoAlchemy
==================

.. image:: https://travis-ci.org/cobrateam/flask-mongoalchemy.png?branch=master
   :target: https://travis-ci.org/cobrateam/flask-mongoalchemy

`Flask <http://flask.pocoo.org>`_ support for `MongoDB <https://mongodb.org>`_ using `MongoAlchemy <http://mongoalchemy.org>`_.

Documentation
+++++++++++++

If you want to get started, check the `example sourcecode <https://github.com/cobrateam/flask-mongoalchemy/tree/master/examples>`_ out.

    For full documentation, see the online docs at: `<https://pythonhosted.org/Flask-MongoAlchemy/>`_.

Development
+++++++++++

* Source hosted at `Github <https://github.com/cobrateam/flask-mongoalchemy>`_
* Report issues on `Github Issues <https://github.com/cobrateam/flask-mongoalchemy/issues>`_

Bootstraping the development environment
----------------------------------------

If you are using a virtualenv, bootstrap your development environment by running:

::

    $ make bootstrap

Running tests
-------------

With all dependencies installed (after bootstrap development env), just run:

::

    $ make test

Community
---------

#cobrateam on chanel irc.freenode.net

Changelog
+++++++++

Flask-MongoAlchemy 0.7.2
------------------------

* Pin pymongo version to ensure driver compatibility.

Flask-MongoAlchemy 0.7.1
------------------------

* Support for specifying the full connection string, via the
  MONGOALCHEMY_CONNECTION_STRING configuration value.

Flask-MongoAlchemy 0.7.0
------------------------

* Multiple database support (thanks Misja Hoebe)

Flask-MongoAlchemy 0.6.1
------------------------

* Replica set support, via the MONGOALCHEMY_REPLICA_SET configuration value.

Flask-MongoAlchemy 0.6.0
------------------------

* Use the not-so-new extension scheme for Flask, users now should import the
  extension using the flask.ext metapackage
* Some fixes in the docs, regarding other extensions usage in examples

Flask-MongoAlchemy 0.5.4
------------------------

* [bugfix] fix compatibility with pymongo 2.2

Flask-MongoAlchemy 0.5.3
------------------------

* [bugfix] fixed a bug on setup.py

Flask-MongoAlchemy 0.5.2
------------------------

* added a configuration flag for user authentication based either on database or server
* [bugfix] fixed server based authentication

Flask-MongoAlchemy 0.5.1
------------------------

* [bugfix] fixed the subpackage structure

Flask-MongoAlchemy 0.5
----------------------

* Support for multiple MongoDB sessions

Flask-MongoAlchemy 0.4.3
------------------------

* [bugfix] added database to MongoDB URI for authenticated connectinos

Flask-MongoAlchemy 0.4.2
------------------------

* Fixed pymongo dependency in setup.py

Flask-MongoAlchemy 0.4.1
------------------------

* MongoAlchemy 0.9 as dependency
* [bugfix] safe session operations on connect, save and remove

Flask-MongoAlchemy 0.4
----------------------

* Documentation improvements
* Support for safe or unsafe sessions and operations

Flask-MongoAlchemy 0.3.3
------------------------

* Fixed dependencies on ``setup.py``

Flask-MongoAlchemy 0.3.2
------------------------

* Compatibility with Flask 0.7

Flask-MongoAlchemy 0.3.1
------------------------

* [bugfix] method ``get`` on ``Query`` objects was never returning the object

Flask-MongoAlchemy 0.3
----------------------

* Introduced update queries support

Flask-MongoAlchemy 0.2
----------------------

* Reverse compatibility broken on ``Document`` class. The ``get()`` method was moved to ``BaseQuery`` class.
  Here the old code, on version ``0.1``: ::

    >>> Document.get(mongo_id)

  And the new code, on version ``0.2``: ::

    >>> Document.query.get(mongo_id)

* Added ``get_or_404``, ``first_or_404`` and ``paginate`` methods on ``BaseQuery`` class. Check the `documentation <https://pythonhosted.org/Flask-MongoAlchemy>`_ to know how to use them :)
