from flask.ext.login import wraps, current_user
from flask import jsonify


def role_required(roles):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if current_user.is_anonymous():
                response = jsonify(BizResponse(
                    success=False,
                    data=None
                ).to_dict())
                response.status_code = 401
                return response
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


class BizResponse():
    success = False
    data = None

    def __init__(self, success=False, data=None, page=1, total=1):
        self.page = page
        self.total = total
        self.success = success
        self.data = data

    def to_dict(self):
        return {
            'success': self.success,
            'page': self.page,
            'total': self.total,
            'data': self.data
        }
