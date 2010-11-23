# -*- coding: utf-8 -*-
"""
    flaskext.mongoalchemy
    ~~~~~~~~~~~~~~~~~~~~~

    Adds Flask support for MongoDB using Mongo-Alchemy.

    :copyright: (c) 2010 by Francisco Souza.
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

from mongoalchemy.document import Document
from mongoalchemy import session
from mongoalchemy import fields

def _include_mongoalchemy(obj):
    for module in session, fields:
        for key in dir(module):
            if not hasattr(obj, key):
                setattr(obj, key, getattr(module, key))

class ImproperlyConfiguredError(Exception):
    pass

class MongoAlchemy(object):
    """Class used to control the MongoAlchemy integration to a Flask application.

    You can use this by providing the Flask app on instantiation or by calling an init_app method
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

        _include_mongoalchemy(self)

        if app is not None:
            self.init_app(app)
        else:
            self.app = None

    def init_app(self, app):
        """This callback can be used to initialize an application for the use with this
        MongoDB setup. Never use a database in the context of an application not
        initialized that way or connections will leak."""
        if 'MONGOALCHEMY_DATABASE' not in app.config:
            raise ImproperlyConfiguredError("You should provide a database name (the MONGOENGINE_DATABASE setting).")

        app.config.setdefault('MONGOALCHEMY_SERVER', 'localhost')
        app.config.setdefault('MONGOALCHEMY_PORT', '27017')
        app.config.setdefault('MONGOALCHEMY_USER', None)
        app.config.setdefault('MONGOALCHEMY_PASSWORD', None)

        self.app = app

