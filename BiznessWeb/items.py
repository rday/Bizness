from flask import Blueprint, jsonify, request, abort
from werkzeug.exceptions import BadRequest
from Bizness import db
from Bizness.models import Item
from .api import BizResponse
from config import PAGE_SIZE
import iso8601


items_bp = Blueprint('items_bp', __name__, url_prefix='/items')


@items_bp.route('/')
def index():
    """
    request.args inherits from TypeConversionDict !
    """
    page_size = request.args.get('page_size', PAGE_SIZE, type=int)
    page = request.args.get('page', 1, type=int)
    last_date = request.args.get('last_date', None, type=lambda d: iso8601.parse_date(d))

    if last_date is None:
        items_pagination = Item.paginate(page, page_size)
    else:
        items_pagination = Item.paginate_by_due_date(last_date, page_size)

    items = {
        'items': [item.to_dict() for item in items_pagination.items]
    }

    response = BizResponse(
        success=True,
        data=items,
        total=items_pagination.total,
        page=items_pagination.page
    )

    return jsonify(response.to_dict())


@items_bp.route('/', methods=['POST'])
def create_item():
    try:
        new_item = Item.from_request(request)
        db.session.add(new_item)
        db.session.commit()

        response = BizResponse(
            success=True,
            data=new_item.to_dict(),
            total=1
        )
    except BadRequest as e:
        response = BizResponse(
            success=False,
            data=e.description
        )
    except Exception:
        response = BizResponse(
            success=False,
            data='An error occurred saving the item'
        )

    return jsonify(response.to_dict())


@items_bp.route('/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.filter(Item.id == item_id).first()
    if item is None:
        abort(404)

    response = BizResponse(
        success=True,
        data=item.to_dict()
    )

    return jsonify(response.to_dict())
