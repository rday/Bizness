from . import db
from datetime import datetime


class Task():
    name = u''
    description = u''
    due_due = None
    item_list = None

    def __init__(self, name, description, due_date=None):
        self.name = name
        self.description = description
        self.due_due = due_date
        self.item_list = []

    def __str__(self):
        return u"Task <{}>".format(self.name)

    def add_item(self, task):
        self.item.append(task)


class Item():
    name = u''
    description = u''
    handled = False


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.Text)
    handled = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.TIMESTAMP)
    handled_date = db.Column(db.TIMESTAMP)

    def handle(self):
        self.handled_date = datetime.utcnow()
        self.handled = True

    def __str__(self):
        return u"Item <{}>".format(self.name)
