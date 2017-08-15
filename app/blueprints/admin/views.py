from flask import url_for, request
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from werkzeug.utils import redirect

from app.models import Message


class AdminOnlyMixin:
    def is_accessible(self):
        return hasattr(current_user, 'is_admin') and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


class AdminOnlyModelView(AdminOnlyMixin, ModelView):
    pass


class MessagesView(AdminOnlyMixin, BaseView):
    @expose('/')
    def index(self):
        messages = Message.query.filter_by(acknowledged=False)
        return self.render('admin/message.html', messages=messages)
