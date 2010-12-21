from collection import db

class Book(db.Document):
    title = db.StringField()
    year = db.IntField()
