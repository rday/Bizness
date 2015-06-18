"""The Bizness web package.

This package provides a web interface to the Bizness package functionality.
"""


import config
from flask import Flask
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.login import LoginManager
from .items import items_bp
from .tasks import tasks_bp
from Bizness import db
from Bizness.models import Item, Task


app = Flask(__name__)
app.config.from_object(config)

# Setup our database with the config file loaded
db.init_app(app)

# Setup admin
admin = Admin(app)
admin.add_view(ModelView(Item, db.session))
admin.add_view(ModelView(Task, db.session))

# Setup the login manager
# For authentication
lm = LoginManager()
lm.init_app(app)
lm.login_view = "/login"
app.secret_key = app.config['SECRET_KEY']

# Setup our route blueprints
app.register_blueprint(items_bp)
app.register_blueprint(tasks_bp)
