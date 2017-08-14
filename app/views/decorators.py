from flask import abort
from flask_login import current_user
from functools import wraps

def remove_xss_protection(response):
    response.headers['X-XSS-Protection'] = 0
    return response


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_admin:
            func(*args, **kwargs)
        else:
            abort(401)

    return wrapper
