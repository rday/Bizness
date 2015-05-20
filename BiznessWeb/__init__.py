"""The Bizness web package.

This package provides a web interface to the Bizness package functionality.
"""


import config
from flask import Flask
from .items import items_bp


app = Flask(__name__)
app.config.from_object(config)

app.register_blueprint(items_bp)
