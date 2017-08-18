from flask import url_for, request
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from werkzeug.utils import redirect

from app.models import Message
from app.blueprints.decorators import is_admin_user


class AdminOnlyMixin:
    def is_accessible(self):
        return is_admin_user(current_user)

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('authentication.login', next=request.url))


class AdminOnlyModelView(AdminOnlyMixin, ModelView):
    pass


class MessagesView(AdminOnlyMixin, BaseView):
    @expose('/')
    def index(self):
        messages = Message.query.filter_by(acknowledged=False)
        return self.render('admin/message.html', messages=messages)
