# -*- coding: utf-8 -*-

# Copyright 2010 flask-mongoalchemy authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from flask import Flask
from mongoalchemy import fields
from mongoalchemy.session import Session

from flask.ext.mongoalchemy import BaseQuery, ImproperlyConfiguredError, MongoAlchemy
from tests import BaseTestCase


class MongoAlchemyObjectTestCase(BaseTestCase):
    "MongoAlchemy itself object tests"

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['MONGOALCHEMY_DATABASE'] = 'testing'
        self.app.config['TESTING'] = True

    def tearDown(self):
        del(self.app)

    def test_should_provide_a_Document_class_to_be_extended_inside_the_MongoAlchemy_object(self):
        db = MongoAlchemy()
        assert db.Document is not None

    def test_should_provide_a_query_object_for_queries_on_a_document(self):
        db = MongoAlchemy(self.app)

        class Todo(db.Document):
            description = db.StringField()

        self.assertIsInstance(Todo.query, BaseQuery)

    def test_should_provide_a_session_object_on_mongoalchemy_instance(self):
        db = MongoAlchemy(self.app)
        self.assertIsInstance(db.session, Session)

    def test_should_be_possible_to_create_a_customized_query_class(self):
        db = MongoAlchemy(self.app)

        class Query(BaseQuery):
            pass

        class Todo(db.Document):
            description = db.StringField()
            query_class = Query

        self.assertIsInstance(Todo.query, Query)

    def test_should_set_None_to_query_attribute_on_Document_when_queryclass_does_not_extends_BaseQuery(self):
        db = MongoAlchemy()

        class Query(object):
            pass

        class Todo(db.Document):
            description = db.StringField()
            query_class = Query

        assert Todo.query is None

    def test_should_include_all_mongo_alchemy_fields_objects(self):
        db = MongoAlchemy()
        for key in dir(fields):
            assert hasattr(db, key), "should have the %s attribute" % key
        assert hasattr(db, 'DocumentField'), "should have the DocumentField attribute"

    def test_should_be_able_to_instantiate_passing_the_app(self):
        db = MongoAlchemy(self.app)
        assert db.session is not None

    def test_should_be_able_to_instantiate_without_passing_the_app_and_set_it_later(self):
        db = MongoAlchemy()
        assert db.session is None
        db.init_app(self.app)
        assert db.session is not None

    def test_should_contain_a_not_none_query(self):
        "Document.query should never be None"
        db = MongoAlchemy()
        db.init_app(self.app)

        class Person(db.Document):
            name = db.StringField()

        p = Person()
        assert p.query is not None

    def test_should_not_be_able_to_work_without_providing_a_database_name(self):
        with self.assertRaises(ImproperlyConfiguredError):
            app = Flask(__name__)
            MongoAlchemy(app)

    def test_should_be_able_to_work_without_providing_server_port_user_and_password_for_database_connection(self):
        app = Flask(__name__)
        app.config['MONGOALCHEMY_DATABASE'] = 'my_database'
        MongoAlchemy(app)
        self.assertEqual(app.config['MONGOALCHEMY_SERVER'], 'localhost')
        self.assertEqual(app.config['MONGOALCHEMY_PORT'], '27017')
        self.assertEqual(app.config['MONGOALCHEMY_USER'], None)
        self.assertEqual(app.config['MONGOALCHEMY_PASSWORD'], None)

    def test_should_be_able_to_create_two_decoupled_mongoalchemy_instances(self):
        app = Flask(__name__)
        app.config['MONGOALCHEMY_DATABASE'] = 'my_database'
        db1 = MongoAlchemy(app)
        db2 = MongoAlchemy(app)
        assert db1.Document is not db2.Document, "two documents should not be the same object"
