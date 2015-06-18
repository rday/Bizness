from flask import Blueprint, jsonify, request, abort
from werkzeug.exceptions import BadRequest
from Bizness import db
from Bizness.models import Task
from .api import BizResponse
from config import PAGE_SIZE
import iso8601


tasks_bp = Blueprint('tasks_bp', __name__, url_prefix='/tasks')


@tasks_bp.route('/')
def index():
    """
    request.args inherits from TypeConversionDict !
    """
    page_size = request.args.get('page_size', PAGE_SIZE, type=int)
    page = request.args.get('page', 1, type=int)
    last_date = request.args.get('last_date', None, type=lambda d: iso8601.parse_date(d))

    if last_date is None:
        tasks_pagination = Task.paginate(page, page_size)
    else:
        tasks_pagination = Task.paginate_by_due_date(last_date, page_size)

    tasks = {
        'tasks': [task.to_dict() for task in tasks_pagination.items]
    }

    response = BizResponse(
        success=True,
        data=tasks,
        total=tasks_pagination.total,
        page=tasks_pagination.page
    )

    return jsonify(response.to_dict())


@tasks_bp.route('/', methods=['POST'])
def create_task():
    try:
        new_task = Task.from_request(request)
        db.session.add(new_task)
        db.session.commit()

        response = BizResponse(
            success=True,
            data=new_task.to_dict(),
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
            data='An error occurred saving the task'
        )

    return jsonify(response.to_dict())


@tasks_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.filter(Task.id == task_id).first()
    if task is None:
        abort(404)

    response = BizResponse(
        success=True,
        data=task.to_dict()
    )

    return jsonify(response.to_dict())
