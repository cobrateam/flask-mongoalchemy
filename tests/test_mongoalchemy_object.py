from tests import BaseTestCase
from nose.tools import assert_true, assert_equals, raises
from flask import Flask
from flaskext.mongoalchemy import ImproperlyConfiguredError

class MongoAlchemyObjectTestCase(BaseTestCase):

    def setup(self):
        self.app = Flask('testing')
        self.app.config['MONGOALCHEMY_DATABASE'] = 'testing'
        self.app.config['TESTING'] = True

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

    @raises(ImproperlyConfiguredError)
    def test_shout_not_be_able_to_work_without_providing_a_database_name(self):
        from flaskext.mongoalchemy import MongoAlchemy
        app = Flask('new_test')
        db = MongoAlchemy(app)

    def should_be_able_to_work_without_providing_server_port_user_and_password_for_database_connection(self):
        from flaskext.mongoalchemy import MongoAlchemy
        app = Flask('newest_test')
        app.config['MONGOALCHEMY_DATABASE'] = 'my_database'
        db = MongoAlchemy(app)
        assert_equals(app.config['MONGOALCHEMY_SERVER'], 'localhost')
        assert_equals(app.config['MONGOALCHEMY_PORT'], '27017')
        assert_equals(app.config['MONGOALCHEMY_USER'], None)
        assert_equals(app.config['MONGOALCHEMY_PASSWORD'], None)

    def teardown(self):
        del(self.app)
