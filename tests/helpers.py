def _make_todo_document(db):
    class Todo(db.Document):
        description = db.StringField()
    return Todo
