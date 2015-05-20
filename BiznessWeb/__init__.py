"""The Bizness web package.

This package provides a web interface to the Bizness package functionality.
"""


import config
from flask import Flask
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from .items import items_bp
from Bizness import db
from Bizness.models import Item


app = Flask(__name__)
app.config.from_object(config)

# Setup our database with the config file loaded
db.init_app(app)

# Setup admin
admin = Admin(app)
admin.add_view(ModelView(Item, db.session))

# Setup our route blueprints
app.register_blueprint(items_bp)
