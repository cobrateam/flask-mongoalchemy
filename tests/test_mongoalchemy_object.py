from tests import BaseTestCase
from nose.tools import assert_true, assert_equals

class MongoAlchemyObjectTestCase(BaseTestCase):

    def setup(self):
        from flask import Flask
        self.app = Flask('testing')

    def should_provide_a_Document_class_to_be_extended_inside_the_MongoAlchemy_object(self):
        from flaskext.mongoalchemy import MongoAlchemy
        db = MongoAlchemy()
        assert db.Document is not None

    def should_include_all_mongoalchemy_session_objects_and_mongo_alchemy_fields_objects(self):
        from mongoalchemy import session
        from mongoalchemy import fields
        from flaskext.mongoalchemy import MongoAlchemy

        db = MongoAlchemy()
        for module in session, fields:
            for key in dir(module):
                assert_true(hasattr(db, key))

    def should_be_able_to_instantiate_passing_the_app(self):
        from flaskext.mongoalchemy import MongoAlchemy
        db = MongoAlchemy(self.app)
        assert_equals(db.app, self.app)

    def should_be_able_to_instantiate_without_passing_the_app_and_set_it_later(self):
        from flaskext.mongoalchemy import MongoAlchemy
        db = MongoAlchemy()
        assert db.app is None
        db.init_app(self.app)
        assert_equals(db.app, self.app)
