from flask import abort
from flask_login import current_user
from functools import wraps


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if hasattr(current_user, 'is_admin') and current_user.is_admin:
            return func(*args, **kwargs)
        else:
            abort(401)

    return wrapper
