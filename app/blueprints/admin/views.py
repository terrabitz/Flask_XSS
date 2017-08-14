from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user

from app.models import User
from app.blueprints.decorators import admin_required

admin = Blueprint('admin', __name__, template_folder='templates')


@admin.route('/')
@login_required
@admin_required
def index():
    return render_template('admin/index.html')



@admin.route('/messages', methods=['POST', 'GET'])
@login_required
@admin_required
def messages():
    return render_template('admin/message.html')

