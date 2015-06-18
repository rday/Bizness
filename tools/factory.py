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
