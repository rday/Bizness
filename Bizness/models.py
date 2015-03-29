from . import db
from datetime import datetime


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
