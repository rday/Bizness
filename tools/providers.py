"""
https://github.com/joke2k/faker/issues/170 highlights an error with US phone numbers.
The first example shows a quick patch to fix this bug without relying on an upstream fix.

For fields that aren't present in the Faker package, we can always use lorem ipsum to
fill in text. But its nice to have more realistic values. The second example demonstrates
how we can setup providers for our own fields that aren't present in the Faker package.
(Job actually is, but our provider formats the titles a little different).
"""
from Bizness import models
from BiznessWeb import app, db
from mixer.backend.flask import Mixer
from faker.providers.phone_number import Provider as BaseProvider


class FixedPhoneNumberProvider(BaseProvider):
    formats = (
        '###-###-####',
        '(###)###-####',
        '1-###-###-####',
        '###.###.####',
        '###-###-####x###',
        '(###)###-####x###',
        '1-###-###-####x###',
        '###.###.####x###',
        '###-###-####x####',
        '(###)###-####x####',
        '1-###-###-####x####',
        '###.###.####x####',
        '###-###-####x#####',
        '(###)###-####x#####',
        '1-###-###-####x#####',
        '###.###.####x#####'
    )


class JobTitleProvider(BaseProvider):
    formats = ['{{experience_level}} {{job_type}}', ]

    job_types = ['Developer', 'QA Analyst', 'UX Designer']

    experience_levels = ['', 'Senior', 'Junior', 'Intern']

    def title(self):
        pattern = self.random_element(self.formats)
        return self.generator.parse(pattern)

    @classmethod
    def job_type(cls):
        return cls.random_element(cls.job_types)

    @classmethod
    def experience_level(cls):
        return cls.random_element(cls.experience_levels)


mixer = Mixer(locale='en_US', commit=False)

with app.app_context():
    db.drop_all()
    db.create_all()

    mixer.init_app(app)
    mixer.faker.add_provider(JobTitleProvider)
    mixer.faker.add_provider(FixedPhoneNumberProvider)
    mixer.register(models.User, phone_number=mixer.faker.phone_number)

    for user in mixer.cycle(20).blend(models.User):
        print("{} {}: {} {}".format(user.first_name, user.last_name, user.title, user.phone_number))
