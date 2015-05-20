"""The Bizness package.

This package provides us with the ability to store and track bizness items.
It also lets us handle those items.

This package is distinct from the web package because we want to clearly
separate responsibility. We may need to call Bizness methods from a cron
job. Maybe a message queue runs methods periodically. Maybe we are building
a second version of our public API and we need to access Bizness methods
without modifying the original API routes.

As applications grow, you add reports. Reports tend to be multiple ways of
looking at the same data. This means that you can end up Repeating Yourself
if you have a lot of logic in the web route. If the web routes always call
the Bizness package, it provides one canonical place to deal with data.
"""

from .models import Item


item_list = [
    Item(
        name='Item 1',
        description='Description 1'
    ),
    Item(
        name='Item 2',
        description='Description 2'
    ),
    Item(
        name='Item 3',
        description='Description 3'
    )
]