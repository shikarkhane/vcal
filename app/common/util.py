import json
import decimal

from flywheel.model_meta import ModelMetaclass
import time

from threading import Thread
from functools import wraps

from app.common.bl import getAllUsers


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, ModelMetaclass):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and not x.endswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    # if isinstance(data, datetime.date):
                    #     x = data
                    #     data = datetime.datetime.strftime(data, '%Y-%m-%d')
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields
        if isinstance(obj, decimal.Decimal):
            return float(obj)

        return json.JSONEncoder.default(self, obj)


class DateUtil():
    def __init__(self):
        pass
    def getHumanDate(self, epoch):
        return time.strftime("%A, %d %B %Y", time.localtime(epoch))
    def isAWeekend(self, epoch):
        x = time.localtime(epoch)
        if x.tm_wday in [5,6]:
            return True
        else:
            return False

class UserUtil():
    def __init__(self, group_id):
        self.users = getAllUsers(group_id)
        self.users_dict = {u['id'] : u for u in self.users}
    def getName(self, user_id):
        return self.users_dict[user_id]['name']
    def getEmail(self, user_id):
        return self.users_dict[user_id]['email']

def run_async(func):
    @wraps(func)
    def async_func(*args, **kwargs):
        func_hl = Thread(target = func, args = args, kwargs = kwargs)
        func_hl.start()
        return func_hl

    return async_func