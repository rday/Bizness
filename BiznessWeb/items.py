from flask import Blueprint, jsonify
from Bizness.items import list_items


items_bp = Blueprint('items_bp', __name__)

@items_bp.route('/')
def index():
    items = {
        'items': [str(x) for x in list_items()]
    }

    return jsonify(items)