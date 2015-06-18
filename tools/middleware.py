from Bizness import models
from BiznessWeb import app, db
from mixer.backend.flask import Mixer
from flask.ext.bcrypt import Bcrypt


mixer = Mixer(locale='en_US', commit=False)
bcrypt = Bcrypt(app)


@mixer.middleware(models.User)
def encrypt_password(user):
    user.password = bcrypt.generate_password_hash('def4ult')
    return user


with app.app_context():
    db.drop_all()
    db.create_all()

    mixer.init_app(app)
    mixer.register(models.User, email_address=mixer.faker.email_address)

    for user in mixer.cycle(20).blend(models.User):
        print(u"{} {}: {}({})".format(user.first_name, user.last_name, user.email_address, user.password))
