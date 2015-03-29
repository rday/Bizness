from models import Item


def list_items():
    return Item.query.all()