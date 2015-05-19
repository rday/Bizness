from config import PAGE_SIZE


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
