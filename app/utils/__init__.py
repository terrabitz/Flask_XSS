from flask import redirect, url_for, request
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView

from app.models import User


class AdminOnlyModelView(ModelView):
    def is_accessible(self):
        return hasattr(current_user, 'is_admin') and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


def snake_to_title(string):
    return ' '.join([word.capitalize() for word in string.split('_')])


def load_user(user_id):
    return User.query.filter_by(id=user_id).first()
