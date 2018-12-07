import logging
from flask import request, session
import login_utils

def trace(fn):
    from functools import wraps
    import inspect
    @wraps(fn)
    def wrapper(*args, **kwargs):
        logging.getLogger(__name__).info('RECEIVED  {} {} {}'.format(request.method, request.path, login_utils.get_login_info()))
        out = apply(fn, args, kwargs)
        logging.getLogger(__name__).info('COMPLETED {} {} {}'.format(request.method, request.path, login_utils.get_login_info()))
        return out
    return wrapper
