import datetime
from random import randint
from Bizness import models
from BiznessWeb import app, db
from mixer.backend.flask import mixer


with app.app_context():
    db.drop_all()
    db.create_all()
    mixer.init_app(app)

    for task in mixer.cycle(10).blend(models.Task,
                                      name=mixer.faker.name,
                                      description=mixer.faker.text):
        task.due_date = datetime.datetime.utcnow() + datetime.timedelta(days=randint(5, 10))
        db.session.add(task)

    db.session.flush()

    for item in mixer.cycle(100).blend(models.Item,
                                       name=mixer.faker.name,
                                       description=mixer.faker.text,
                                       task=mixer.SELECT):
        item.handled = True if randint(0, 1) == 1 else False
        item.due_date = datetime.datetime.utcnow() + datetime.timedelta(days=randint(0, 5) + (365 * 30))
        if item.handled is True:
            item.handled_date = datetime.datetime.utcnow() - datetime.timedelta(days=randint(0, 3))
        db.session.add(item)

    db.session.commit()