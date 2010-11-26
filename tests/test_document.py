from tests import BaseTestCase
from flask import Flask
from flaskext import mongoalchemy
from nose.tools import assert_equals

def _make_todo_document(db):
    class Todo(db.Document):
        description = db.StringField()
    return Todo

class MongoAlchemyDocumentTestCase(BaseTestCase):
    "MongoAlchemy documents tests"

    def setup(self):
        self.app = Flask(__name__)
        self.app.config['MONGOALCHEMY_DATABASE'] = 'testing'
        self.app.config['TESTING'] = True
        self.db = mongoalchemy.MongoAlchemy(self.app)
        self.Todo = _make_todo_document(self.db)

    def teardown(self):
        for todo in self.Todo.query.all():
            todo.delete()

    def should_be_able_to_save_a_document_on_database_by_calling_its_save_method(self):
        "A document should be able to save itself in the database by calling it's \"save()\" method"
        todo = self.Todo(description=u'Reinvent the world')
        todo.save()
        assert_equals(self.Todo.query.count(), 1)

    def should_be_able_to_delete_a_document_on_database_by_calling_its_delete_method(self):
        "A document should be able to delete itself in the database by calling it's \"delete()\" method"
        todo = self.Todo(description=u'Reinvent the world')
        todo.save()
        assert_equals(self.Todo.query.count(), 1)
        todo.delete()
        assert_equals(self.Todo.query.count(), 0)
