# -*- coding: utf-8 -*-

# Copyright 2015 flask-mongoalchemy authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from tests import BaseTestCase
from flask import Flask


class MongoDBURITestCase(BaseTestCase):
    "MongoDB URI generation"

    def setup(self):
        self.app = Flask(__name__)
        self.app.config['MONGOALCHEMY_DATABASE'] = 'test'

    def test_uri_without_database_name(self):
        from flask.ext.mongoalchemy import _get_mongo_uri
        self.assertEqual(_get_mongo_uri(self.app), 'mongodb://localhost:27017/')

    def test_uri_with_user_only(self):
        self.app.config['MONGOALCHEMY_USER'] = 'luke'
        from flask.ext.mongoalchemy import _get_mongo_uri
        self.assertEqual(_get_mongo_uri(self.app), 'mongodb://luke@localhost:27017/')

    def test_uri_with_user_and_password(self):
        self.app.config['MONGOALCHEMY_USER'] = 'luke'
        self.app.config['MONGOALCHEMY_PASSWORD'] = 'father'
        self.app.config['MONGOALCHEMY_SERVER_AUTH'] = False
        from flask.ext.mongoalchemy import _get_mongo_uri
        self.assertEqual(_get_mongo_uri(self.app), 'mongodb://luke:father@localhost:27017/test')

    def test_mongodb_uri_with_external_server(self):
        self.app.config['MONGOALCHEMY_SERVER'] = 'database.lukehome.com'
        self.app.config['MONGOALCHEMY_PORT'] = '42'
        from flask.ext.mongoalchemy import _get_mongo_uri
        self.assertEqual(_get_mongo_uri(self.app), 'mongodb://database.lukehome.com:42/')

    def test_mongodb_uri_with_options(self):
        self.app.config['MONGOALCHEMY_SERVER'] = 'database.lukehome.com'
        self.app.config['MONGOALCHEMY_OPTIONS'] = 'safe=true'
        from flask.ext.mongoalchemy import _get_mongo_uri
        self.assertEqual(_get_mongo_uri(self.app),
                         'mongodb://database.lukehome.com:27017/?safe=true')

    def test_mongodb_uri_connection_string(self):
        self.app.config['MONGOALCHEMY_CONNECTION_STRING'] = uri = 'mongodb://luke@rhost:27018/test'
        from flask.ext.mongoalchemy import _get_mongo_uri
        self.assertEqual(_get_mongo_uri(self.app), uri)
