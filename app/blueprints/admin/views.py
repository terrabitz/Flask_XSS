from flask import url_for, request
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from werkzeug.utils import redirect


class AdminOnlyModelView(ModelView):
    def is_accessible(self):
        return hasattr(current_user, 'is_admin') and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))
