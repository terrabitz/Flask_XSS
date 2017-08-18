from flask import abort
from flask_login import current_user
from functools import wraps


def is_admin_user(user):
    return hasattr(user, 'is_admin') and current_user.is_admin


def is_owning_user(user, id):
    return user.id == id


def is_admin_or_owning_user(id):
    return is_admin_user(current_user) or is_owning_user(current_user, id)


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if is_admin_user(current_user):
            return func(*args, **kwargs)
        else:
            abort(401)

    return wrapper
