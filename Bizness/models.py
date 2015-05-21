from sqlalchemy.exc import NoInspectionAvailable
from sqlalchemy.ext import hybrid
from sqlalchemy.orm.query import Query
from sqlalchemy.inspection import inspect as sqlalchemy_inspect
import uuid
from sqlalchemy.ext.associationproxy import AssociationProxy
from sqlalchemy.orm import RelationshipProperty as RelProperty

import datetime
from . import db
from .reqparse import RequestParser
import iso8601
from flask_sqlalchemy import Pagination


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.Text)
    due_date = db.Column(db.TIMESTAMP)

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
        return u"Task {} <#{}> due {}".format(self.name, self.id, self.due_date.isoformat())


def is_mapped_class(cls):
    """Returns ``True`` if and only if the specified SQLAlchemy model class is
    a mapped class.
    """
    try:
        sqlalchemy_inspect(cls)
        return True
    except:
        return False


def is_like_list(instance, relation):
    """Returns ``True`` if and only if the relation of `instance` whose name is
    `relation` is list-like.
    A relation may be like a list if, for example, it is a non-lazy one-to-many
    relation, or it is a dynamically loaded one-to-many.
    """
    if relation in instance._sa_class_manager:
        return instance._sa_class_manager[relation].property.uselist
    elif hasattr(instance, relation):
        attr = getattr(instance._sa_instance_state.class_, relation)
        if hasattr(attr, 'property'):
            return attr.property.uselist
    related_value = getattr(type(instance), relation, None)
    if isinstance(related_value, AssociationProxy):
        local_prop = related_value.local_attr.prop
        if isinstance(local_prop, RelProperty):
            return local_prop.uselist


# Taken from the Flask Restless to_dict function
# https://github.com/jfinkels/flask-restless/blob/master/flask_restless/helpers.py#L270
class DictSerializer(db.Model):
    __abstract__ = True

    def to_dict(instance, deep=None, exclude=None, include=None,
                exclude_relations=None, include_relations=None,
                include_methods=None):

        COLUMN_BLACKLIST = ('_sa_polymorphic_on', )

        if (exclude is not None or exclude_relations is not None) and \
                (include is not None or include_relations is not None):
            raise ValueError('Cannot specify both include and exclude.')
        # create a list of names of columns, including hybrid properties
        instance_type = type(instance)
        columns = []
        try:
            inspected_instance = sqlalchemy_inspect(instance_type)
            column_attrs = inspected_instance.column_attrs.keys()
            descriptors = inspected_instance.all_orm_descriptors.items()
            hybrid_columns = [k for k, d in descriptors
                              if d.extension_type == hybrid.HYBRID_PROPERTY
                              and not (deep and k in deep)]
            columns = column_attrs + hybrid_columns
        except NoInspectionAvailable:
            return instance
        # filter the columns based on exclude and include values
        if exclude is not None:
            columns = (c for c in columns if c not in exclude)
        elif include is not None:
            columns = (c for c in columns if c in include)
        # create a dictionary mapping column name to value
        result = dict((col, getattr(instance, col)) for col in columns
                      if not (col.startswith('__') or col in COLUMN_BLACKLIST))
        # add any included methods
        if include_methods is not None:
            for method in include_methods:
                if '.' not in method:
                    value = getattr(instance, method)
                    # Allow properties and static attributes in include_methods
                    if callable(value):
                        value = value()
                    result[method] = value
        # Check for objects in the dictionary that may not be serializable by
        # default. Convert datetime objects to ISO 8601 format, convert UUID
        # objects to hexadecimal strings, etc.
        for key, value in result.items():
            if isinstance(value, (datetime.date, datetime.time)):
                result[key] = value.isoformat()
            elif isinstance(value, uuid.UUID):
                result[key] = str(value)
            elif key not in column_attrs and is_mapped_class(type(value)):
                result[key] = instance.to_dict(value)
        # recursively call _to_dict on each of the `deep` relations
        deep = deep or {}
        for relation, rdeep in deep.items():
            # Get the related value so we can see if it is None, a list, a query
            # (as specified by a dynamic relationship loader), or an actual
            # instance of a model.
            relatedvalue = getattr(instance, relation)
            if relatedvalue is None:
                result[relation] = None
                continue
            # Determine the included and excluded fields for the related model.
            newexclude = None
            newinclude = None
            if exclude_relations is not None and relation in exclude_relations:
                newexclude = exclude_relations[relation]
            elif (include_relations is not None and
                  relation in include_relations):
                newinclude = include_relations[relation]
            # Determine the included methods for the related model.
            newmethods = None
            if include_methods is not None:
                newmethods = [method.split('.', 1)[1] for method in include_methods
                              if method.split('.', 1)[0] == relation]
            if is_like_list(instance, relation):
                result[relation] = [instance.to_dict(inst, rdeep, exclude=newexclude,
                                            include=newinclude,
                                            include_methods=newmethods)
                                    for inst in relatedvalue]
                continue
            # If the related value is dynamically loaded, resolve the query to get
            # the single instance.
            if isinstance(relatedvalue, Query):
                relatedvalue = relatedvalue.one()
            result[relation] = instance.to_dict(relatedvalue, rdeep, exclude=newexclude,
                                       include=newinclude,
                                       include_methods=newmethods)
        return result


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
            order_by(Item.due_date.desc())
        total = items.count()
        items = items.limit(page_size).\
            all()

        return Pagination(
            Item.query,
            1,
            page_size,
            total,
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
