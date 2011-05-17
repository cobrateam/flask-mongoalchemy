Flask-MongoAlchemy
==================

    Version 0.3

`Flask <http://flask.pocoo.org>`_ support for `MongoDB <http://mongodb.org>`_ using `MongoAlchemy <http://mongoalchemy.org>`_.

Documentation
+++++++++++++

If you want to get started, check the `example sourcecode <http://github.com/cobrateam/flask-mongoalchemy/tree/master/examples>`_ out.

    For full documentation, see the online docs at: `<http://packages.python.org/Flask-MongoAlchemy/>`_.

Development
+++++++++++

* Source hosted at `Github <http://github.com/cobrateam/flask-mongoalchemy>`_
* Report issues on `Github Issues <http://github.com/cobrateam/flask-mongoalchemy/issues>`_

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

* Added ``get_or_404``, ``first_or_404`` and ``paginate`` methods on ``BaseQuery`` class. Check the `documentation <http://packages.python.org/Flask-MongoAlchemy>`_ to know how to use them :)
