# -*- coding: utf-8 -*-

# Copyright 2010 flask-mongoalchemy authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from tests import BaseTestCase
from flask import Flask

class MongoDBURITestCase(BaseTestCase):
    "MongoDB URI generation"

    def setup(self):
        self.app = Flask(__name__)
        self.app.config['MONGOALCHEMY_DATABASE'] = 'test'

    def test_should_use_localhost_for_server_and_27017_for_port_when_only_the_database_name_was_specified(self):
        from flaskext.mongoalchemy import _get_mongo_uri
        self.assertEqual(_get_mongo_uri(self.app), 'mongodb://localhost:27017/')

    def test_should_be_able_to_generate_an_uri_using_only_the_username_without_password_and_not_include_the_database_for_server_based_auth(self):
        self.app.config['MONGOALCHEMY_USER'] = 'luke'
        from flaskext.mongoalchemy import _get_mongo_uri
        self.assertEqual(_get_mongo_uri(self.app), 'mongodb://luke@localhost:27017/')

    def test_should_be_able_to_generate_an_uri_using_an_username_and_a_password_including_the_database_for_db_based_auth(self):
        self.app.config['MONGOALCHEMY_USER'] = 'luke'
        self.app.config['MONGOALCHEMY_PASSWORD'] = 'father'
        self.app.config['MONGOALCHEMY_SERVER_AUTH'] = False
        from flaskext.mongoalchemy import _get_mongo_uri
        self.assertEqual(_get_mongo_uri(self.app), 'mongodb://luke:father@localhost:27017/test')

    def test_should_be_able_to_use_not_only_localhost_for_server_and_27017_for_port(self):
        self.app.config['MONGOALCHEMY_SERVER'] = 'database.lukehome.com'
        self.app.config['MONGOALCHEMY_PORT'] = '42'
        from flaskext.mongoalchemy import _get_mongo_uri
        self.assertEqual(_get_mongo_uri(self.app), 'mongodb://database.lukehome.com:42/')

    def test_should_be_able_to_generate_an_uri_with_options(self):
        self.app.config['MONGOALCHEMY_SERVER'] = 'database.lukehome.com'
        self.app.config['MONGOALCHEMY_OPTIONS'] = 'safe=true'
        from flaskext.mongoalchemy import _get_mongo_uri
        self.assertEqual(_get_mongo_uri(self.app), 'mongodb://database.lukehome.com:27017/?safe=true')
