from datetime import datetime
from . import db
from .reqparse import RequestParser
import iso8601
from flask_sqlalchemy import Pagination


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.Text)
    due_due = db.Column(db.TIMESTAMP)

    @staticmethod
    def from_request(request):
        parser = RequestParser()
        parser.add_argument('name', type=str, required=True, help='All items require a name')
        parser.add_argument('description', type=str, help='Short item description')
        parser.add_argument('due_date', type=lambda val, name, op: iso8601.parse_date(val), required=True, help='All items require a due date')

        return Task(**parser.parse_args(request, strict=True))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'due_date': self.due_date.isoformat() if self.due_date else None,
        }

    def __repr__(self):
        return u"Task {} <#{}> due {}".format(self.name, self.id, self.due_due.isoformat())


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer(), primary_key=True)
    task_id = db.Column(db.Integer(), db.ForeignKey('tasks.id'))
    name = db.Column(db.String(64))
    description = db.Column(db.Text)
    handled = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.TIMESTAMP)
    handled_date = db.Column(db.TIMESTAMP)

    task = db.relationship('Task', backref='items')

    def handle(self):
        self.handled_date = datetime.utcnow()
        self.handled = True

    @staticmethod
    def paginate(page, page_size):
        return Item.query.paginate(page, page_size)

    @staticmethod
    def paginate_by_due_date(last_date, page_size):
        items = Item.query.filter(Item.due_date < last_date).\
            order_by(Item.due_date.desc()).\
            limit(page_size).\
            all()

        return Pagination(
            Item.query,
            1,
            page_size,
            len(items),
            items
        )

    @staticmethod
    def from_request(request):
        parser = RequestParser()
        parser.add_argument('task_id', type=int, required=True, help='All items must belong to a task')
        parser.add_argument('name', type=str, required=True, help='All items require a name')
        parser.add_argument('description', type=str, help='Short item description')
        parser.add_argument('handled', type=bool, default=False, help='Whether this has been handled')
        parser.add_argument('due_date', type=lambda val, name, op: iso8601.parse_date(val), required=True, help='All items require a due date')
        parser.add_argument('handled_date', type=lambda val, name, op: iso8601.parse_date(val), help='The date this item was handled')

        return Item(**parser.parse_args(request, strict=True))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'handled': self.handled,
            'handled_date': self.handled_date.isoformat() if self.handled_date else None,
            'task_id': self.task_id,
        }

    def __repr__(self):
        return u"Item {} <#{}> due {}".format(self.name, self.id, self.due_date.isoformat())
