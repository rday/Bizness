"""
Very often, you don't want to remove objects from the database. You simply want
to mark them as inactive so they can be retrieved by the user later. Since most
objects will have an 'active' field, we can use a factory to generate the field
instead of registering a handler for each individual model.

This example demonstrates how to use a custom factory to make 20% of our objects
inactive when they are blended.
"""
from random import randint
from Bizness import models
from BiznessWeb import app, db
from mixer.backend.flask import Mixer
from mixer.backend.sqlalchemy import GenFactory


def fake_active():
    return randint(0, 10) > 2


class MyFactory(GenFactory):
    fakers = GenFactory.fakers
    fakers[('active', bool)] = fake_active


mixer = Mixer(locale='en_US', commit=False, factory=MyFactory)

with app.app_context():
    db.drop_all()
    db.create_all()

    mixer.init_app(app)

    for user in mixer.cycle(20).blend(models.User):
        print("{} {}: {}".format(user.first_name, user.last_name, user.active))
