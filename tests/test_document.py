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
            todo.remove()

    def should_be_able_to_save_a_document_on_database_by_calling_its_save_method(self):
        "A document should be able to save itself in the database by calling it's \"save()\" method"
        todo = self.Todo(description=u'Reinvent the world')
        todo.save()
        assert_equals(self.Todo.query.count(), 1)

    def should_be_able_to_remove_a_document_on_database_by_calling_its_remove_method(self):
        "A document should be able to remove itself in the database by calling it's \"remove()\" method"
        todo = self.Todo(description=u'Reinvent the world')
        todo.save()
        assert_equals(self.Todo.query.count(), 1)
        todo.remove()
        assert_equals(self.Todo.query.count(), 0)

    def should_be_equal_by_the_id(self):
        "Two documents should be equal if they have the same mongo_id"
        todo = self.Todo(description=u'Reinvent the world')
        todo.save()
        my_new_todo = self.Todo(description=u'Save the world')
        my_new_todo.mongo_id = todo.mongo_id
        assert_equals(todo, my_new_todo)

    def should_be_able_to_get_a_document_by_its_mongo_id_via_its_get_method(self):
        todo = self.Todo(description=u'Reinvent the world')
        todo.save()
        searched_todo = self.Todo.get(todo.mongo_id)
        assert_equals(todo, searched_todo)
