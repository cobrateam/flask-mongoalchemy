Flask-MongoAlchemy
==================

    Version 0.2

`Flask <http://flask.pocoo.org>`_ support for `MongoDB <http://mongodb.org>`_ using `MongoAlchemy <http://mongoalchemy.org>`_.

Documentation
+++++++++++++

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

Flask-MongoAlchemy 0.2
----------------------

* Reverse compatibility broken on ``Document`` class. The ``get()`` method was moved to ``BaseQuery`` class.
  Here is the code before the change: ::

    >>> Document.get(mongo_id)

  And the new code: ::

    >>> Document.query.get(mongo_id)
