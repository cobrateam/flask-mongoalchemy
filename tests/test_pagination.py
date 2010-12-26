from tests import BaseTestCase
from tests.helpers import _make_todo_document
from flask import Flask
from flaskext import mongoalchemy

class FlaskMongoAlchemyPaginationTestCase(BaseTestCase):
    "Flask-MongoAlchemy Pagination class"

    def setup(self):
        self.app = Flask(__name__)
        self.app.config['MONGOALCHEMY_DATABASE'] = 'testing'
        self.app.config['TESTING'] = True
        self.db = mongoalchemy.MongoAlchemy(self.app)
        self.Todo = _make_todo_document(self.db)

    def teardown(self):
        for todo in self.Todo.query.all():
            todo.remove()
