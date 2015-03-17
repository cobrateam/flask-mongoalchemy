# -*- coding: utf-8 -*-

# Copyright 2015 flask-mongoalchemy authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from math import ceil
from mongoalchemy import document, exceptions, fields, session, query
from flask import abort

from .meta import make_document_class


def _include_mongoalchemy(obj):
    for key in dir(fields):
        if not hasattr(obj, key):
            setattr(obj, key, getattr(fields, key))
    key = 'DocumentField'
    setattr(obj, key, getattr(document, key))


def _get_mongo_uri(app, key=lambda x:'MONGOALCHEMY_%s' % x):
    app.config.setdefault(key('SERVER'), 'localhost')
    app.config.setdefault(key('PORT'), '27017')
    app.config.setdefault(key('USER'), None)
    app.config.setdefault(key('PASSWORD'), None)
    app.config.setdefault(key('OPTIONS'), None)
    app.config.setdefault(key('REPLICA_SET'), '')

    auth = ''
    database = ''

    uri = app.config.get(key('CONNECTION_STRING'))
    if uri:
        return uri

    if app.config.get(key('USER')) is not None:
        auth = app.config.get(key('USER'))
        if app.config.get(key('PASSWORD')) is not None:
            auth = '%s:%s' % (auth, app.config.get(key('PASSWORD')))
        auth += '@'

        if not app.config.get(key('SERVER_AUTH'), True):
            database = app.config.get(key('DATABASE'))

    options = ''

    if app.config.get(key('OPTIONS')) is not None:
        options = "?%s" % app.config.get(key('OPTIONS'))

    uri = 'mongodb://%s%s:%s/%s%s' % (auth, app.config.get(key('SERVER')),
                                      app.config.get(key('PORT')), database, options)

    return uri


class ImproperlyConfiguredError(Exception):
    """Exception for error on configurations."""
    pass


class _QueryField(object):

    def __init__(self, db):
        self.db = db

    def __get__(self, obj, cls):
        try:
            return cls.query_class(cls, self.db.session)
        except Exception:
            return None


class MongoAlchemy(object):
    """Class used to control the MongoAlchemy integration to a Flask application.

    You can use this by providing the Flask app on instantiation or by calling
    an :meth:`init_app` method an instance object of `MongoAlchemy`. Here an
    example of providing the application on instantiation: ::

        app = Flask(__name__)
        db = MongoAlchemy(app)

    And here calling the :meth:`init_app` method: ::

        db = MongoAlchemy()

        def init_app():
            app = Flask(__name__)
            db.init_app(app)
            return app
    """

    def __init__(self, app=None, config_prefix='MONGOALCHEMY'):
        self.Document = make_document_class(self, Document)
        self.Document.query = _QueryField(self)

        _include_mongoalchemy(self)

        if app is not None:
            self.init_app(app, config_prefix)
        else:
            self.session = None

    def init_app(self, app, config_prefix='MONGOALCHEMY'):
        """This callback can be used to initialize an application for the use with this
        MongoDB setup. Never use a database in the context of an application not
        initialized that way or connections will leak."""

        self.config_prefix = config_prefix
        def key(suffix):
            return '%s_%s' % (config_prefix, suffix)

        if key('DATABASE') not in app.config:
            raise ImproperlyConfiguredError("You should provide a database name "
                                            "(the %s setting)." % key('DATABASE'))

        uri = _get_mongo_uri(app, key)
        rs = app.config.get(key('REPLICA_SET'))
        self.session = session.Session.connect(app.config.get(key('DATABASE')),
                                               safe=app.config.get(key('SAFE_SESSION'),
                                                                   False),
                                               host=uri, replicaSet=rs)
        self.Document._session = self.session


class Pagination(object):
    """Internal helper class returned by :meth:`~BaseQuery.paginate`."""

    def __init__(self, query, page, per_page, total, items):
        #: query object used to create this
        #: pagination object.
        self.query = query
        #: current page number
        self.page = page
        #: number of items to be displayed per page
        self.per_page = per_page
        #: total number of items matching the query
        self.total = total
        #: list of items for the current page
        self.items = items

    @property
    def pages(self):
        """The total number of pages"""
        return int(ceil(self.total / float(self.per_page)))

    @property
    def next_num(self):
        """The next page number."""
        return self.page + 1

    def has_next(self):
        """Returns ``True`` if a next page exists."""
        return self.page < self.pages

    def next(self, error_out=False):
        """Return a :class:`Pagination` object for the next page."""
        return self.query.paginate(self.page + 1, self.per_page, error_out)

    @property
    def prev_num(self):
        """The previous page number."""
        return self.page - 1

    def has_prev(self):
        """Returns ``True`` if a previous page exists."""
        return self.page > 1

    def prev(self, error_out=False):
        """Return a :class:`Pagination` object for the previous page."""
        return self.query.paginate(self.page - 1, self.per_page, error_out)


class BaseQuery(query.Query):
    """
    Base class for custom user query classes.

    This class provides some methods and can be extended to provide a
    customized query class to a user document.

    Here an example: ::

        from flask.ext.mongoalchemy import BaseQuery
        from application import db

        class MyCustomizedQuery(BaseQuery):

            def get_johns(self):
                return self.filter(self.type.first_name == 'John')

        class Person(db.Document):
            query_class = MyCustomizedQuery
            name = db.StringField()

    And you will be able to query the Person model this way: ::

        >>> johns = Person.query.get_johns().first()

    *Note:* If you are extending BaseQuery and writing an ``__init__`` method,
    you should **always** call this class __init__ via ``super`` keyword.

    Here an example: ::

        class MyQuery(BaseQuery):

            def __init__(self, *args, **kwargs):
                super(MyQuery, self).__init__(*args, **kwargs)

    This class is instantiated automatically by Flask-MongoAlchemy, don't
    provide anything new to your ``__init__`` method.
    """

    def __init__(self, type, session):
        super(BaseQuery, self).__init__(type, session)

    def get(self, mongo_id):
        """Returns a :class:`Document` instance from its ``mongo_id`` or ``None``
        if not found"""
        try:
            return self.filter(self.type.mongo_id == mongo_id).first()
        except exceptions.BadValueException:
            return None

    def get_or_404(self, mongo_id):
        """Like :meth:`get` method but aborts with 404 if not found instead of
        returning `None`"""
        document = self.get(mongo_id)
        if document is None:
            abort(404)
        return document

    def first_or_404(self):
        """Returns the first result of this query, or aborts with 404 if the result
        doesn't contain any row"""
        document = self.first()
        if document is None:
            abort(404)
        return document

    def paginate(self, page, per_page=20, error_out=True):
        """Returns ``per_page`` items from page ``page`` By default, it will
        abort with 404 if no items were found and the page was larger than 1.
        This behaviour can be disabled by setting ``error_out`` to ``False``.

        Returns a :class:`Pagination` object."""
        if page < 1 and error_out:
            abort(404)

        items = self.skip((page - 1) * per_page).limit(per_page).all()

        if len(items) < 1 and page != 1 and error_out:
            abort(404)

        return Pagination(self, page, per_page, self.count(), items)


class Document(document.Document):
    "Base class for custom user documents."

    #: the query class used. The :attr:`query` attribute is an instance
    #: of this class. By default :class:`BaseQuery` is used.
    query_class = BaseQuery

    #: an instance of :attr:`query_class`. Used to query the database
    #: for instances of this document.
    query = None

    def save(self, safe=None):
        """Saves the document itself in the database.

        The optional ``safe`` argument is a boolean that specifies if the
        remove method should wait for the operation to complete.
        """
        self._session.insert(self, safe=safe)
        self._session.flush()

    def remove(self, safe=None):
        """Removes the document itself from database.

        The optional ``safe`` argument is a boolean that specifies if the
        remove method should wait for the operation to complete.
        """
        self._session.remove(self, safe=None)
        self._session.flush()

    def __eq__(self, other):
        return isinstance(other, type(self)) and \
            self.has_id() and other.has_id() and \
            self.mongo_id == other.mongo_id
