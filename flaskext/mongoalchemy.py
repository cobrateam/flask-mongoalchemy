# -*- coding: utf-8 -*-
"""
    flaskext.mongoalchemy
    ~~~~~~~~~~~~~~~~~~~~~

    Adds Flask support for MongoDB using Mongo-Alchemy.

    :copyright: (c) 2010 by Francisco Souza.
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

from mongoalchemy import query
from mongoalchemy import document
from mongoalchemy import session
from mongoalchemy import fields

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

class BaseQuery(query.Query):
    pass

class Document(document.Document):
    "Base class for custom user documents."

    #: the query class used. The :attr:`query` attribute is an instance
    #: of this class. By default :class:BaseQuery is used.
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

    @classmethod
    def get(cls, mongo_id):
        """Returns a document instance from its mongo_id"""
        query = cls._session.query(cls)
        return query.filter(cls.mongo_id==mongo_id).first()

    def __cmp__(self, other):
        if isinstance(other, type(self)) and self.has_id() and other.has_id():
            return self.mongo_id.__cmp__(other.mongo_id)
        else:
            return -1
