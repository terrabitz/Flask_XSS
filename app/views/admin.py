from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user

from app.models import User
from app.views.decorators import admin_required

SUPER_SECURE_ADMIN_CREDS = ('admin', 'admin')

admin = Blueprint('admin', __name__)


@admin.route('/')
@login_required
@admin_required
def index():
    return render_template('admin_index.html')


@admin.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    elif request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('index'))
        else:
            return render_template('admin_login.html', error='There was a problem logging in')

    else:
        return render_template('admin_login.html')


@admin.route('/messages', methods=['POST', 'GET'])
@login_required
@admin_required
def messages():
    pass


@admin.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    return redirect(url_for('index'))
