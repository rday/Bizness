class Item():
    name = ''
    description = ''
    handled = False

    def __init__(self, name, description, handled=False):
        self.name = name
        self.description = description
        self.handled = handled

    def __str__(self):
        return u"Item <{}>".format(self.name)

    def handle(self):
        self.handled = True
        return True