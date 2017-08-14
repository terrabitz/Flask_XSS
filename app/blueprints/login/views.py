from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import current_user, login_user, logout_user

from app.models import User

authentication = Blueprint('authentication', __name__, template_folder='templates')


@authentication.route('/login', methods=['POST', 'GET'])
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
            return render_template('login/login.html', error='There was a problem logging in')

    else:
        return render_template('login/login.html')


@authentication.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    return redirect(url_for('index'))
