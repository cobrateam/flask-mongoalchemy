# -*- coding: utf-8 -*-
"""
    flaskext.mongoalchemy
    ~~~~~~~~~~~~~~~~~~~~~

    Adds Flask support for MongoDB using Mongo-Alchemy.

    :copyright: (c) 2010 by Francisco Souza.
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

from math import ceil
from mongoalchemy import query
from mongoalchemy import document
from mongoalchemy import session
from mongoalchemy import fields
from flask import abort

def _include_mongoalchemy(obj):
    for key in dir(fields):
        if not hasattr(obj, key):
            setattr(obj, key, getattr(fields, key))
    key = 'DocumentField'
    setattr(obj, key, getattr(document, key))

def _get_mongo_uri(app):
    app.config.setdefault('MONGOALCHEMY_SERVER', 'localhost')
    app.config.setdefault('MONGOALCHEMY_PORT', '27017')
    app.config.setdefault('MONGOALCHEMY_USER', None)
    app.config.setdefault('MONGOALCHEMY_PASSWORD', None)

    auth = ''

    if app.config.get('MONGOALCHEMY_USER') is not None:
        auth = app.config.get('MONGOALCHEMY_USER')
        if app.config.get('MONGOALCHEMY_PASSWORD') is not None:
            auth = '%s:%s' % (auth, app.config.get('MONGOALCHEMY_PASSWORD'))
        auth += '@'

    uri = 'mongodb://%s%s:%s' %(auth, app.config.get('MONGOALCHEMY_SERVER'),
                                app.config.get('MONGOALCHEMY_PORT'))
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
        except Exception, e:
            return None

class MongoAlchemy(object):
    """Class used to control the MongoAlchemy integration to a Flask application.

    You can use this by providing the Flask app on instantiation or by calling an :meth:`init_app` method
    an instance object of `MongoAlchemy`. Here a sample of providing the application on instantiation: ::

        app = Flask(__name__)
        db = MongoAlchemy(app)

    And here calling the :meth:`init_app` method: ::

        db = MongoAlchemy()

        def init_app():
            app = Flask(__name__)
            db.init_app(app)
            return app
    """

    def __init__(self, app=None):
        self.Document = Document
        self.Document.query = _QueryField(self)

        _include_mongoalchemy(self)

        if app is not None:
            self.init_app(app)
        else:
            self.session = None

    def init_app(self, app):
        """This callback can be used to initialize an application for the use with this
        MongoDB setup. Never use a database in the context of an application not
        initialized that way or connections will leak."""
        if 'MONGOALCHEMY_DATABASE' not in app.config:
            raise ImproperlyConfiguredError("You should provide a database name (the MONGOALCHEMY_DATABASE setting).")

        uri = _get_mongo_uri(app)
        self.session = session.Session.connect(app.config.get('MONGOALCHEMY_DATABASE'), host=uri)
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
    """Base class for custom user query classes.

    This class provides some methods and can be extended to provide a customized query class to a user document.

    Here an example: ::

        from flaskext.mongoalchemy import BaseQuery
        from application import db

        class MyCustomizedQuery(BaseQuery):

            def get_johns(self):
                return self.filter({ 'first_name' : 'John' })

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

    This class is instantiated automatically by Flask-MongoAlchemy, don't provide anything new to your ``__init__`` method."""

    def __init__(self, type, session):
        super(BaseQuery, self).__init__(type, session)

    def get(self, mongo_id):
        """Returns a :class:`Document` instance from its ``mongo_id`` or ``None``
        if not found"""
        return self.filter({'mongo_id' : mongo_id}).first()

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

    def save(self):
        """Saves the document itself in the database."""
        self._session.insert(self)
        self._session.flush()

    def remove(self):
        """Removes the document itself from database."""
        self._session.remove(self)
        self._session.flush()

    def __cmp__(self, other):
        if isinstance(other, type(self)) and self.has_id() and other.has_id():
            return self.mongo_id.__cmp__(other.mongo_id)
        else:
            return -1
