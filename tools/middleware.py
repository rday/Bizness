"""
This example demonstrates the difference between registering a function for a
single field and using middleware to generate field data.

The User middleware could easily be a registered function, just like the
email_address function. But the Item middleware shows how two fields that
are dependent on each other need more than a registered function.
"""
from Bizness import models
from BiznessWeb import app, db
from mixer.backend.flask import Mixer
from flask.ext.bcrypt import Bcrypt
from random import randint


mixer = Mixer(locale='en_US', commit=False)
bcrypt = Bcrypt(app)


@mixer.middleware(models.User)
def encrypt_password(user):
    user.password = bcrypt.generate_password_hash('def4ult')
    return user


@mixer.middleware(models.Item)
def item_handled(item):
    # Handled and handled date are dependent on each other. Middleware
    # gives us a good way to make sure these fields make sense.
    if randint(0, 10) > 2:
        item.handled = True
        item.handled_date = mixer.faker.datetime()

    print(item)
    return item


with app.app_context():
    db.drop_all()
    db.create_all()

    mixer.init_app(app)
    mixer.register(models.User, email_address=mixer.faker.email_address)

    mixer.cycle(10).blend(models.Item, due_date=mixer.faker.datetime)

    for user in mixer.cycle(20).blend(models.User):
        print(u"{} {}: {}({})".format(user.first_name, user.last_name, user.email_address, user.password))
