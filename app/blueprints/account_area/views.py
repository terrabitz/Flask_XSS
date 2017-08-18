from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from app.models import User, Message, db

account_area = Blueprint('account_area', __name__, template_folder='templates')


@account_area.route('/')
@login_required
def index():
    return render_template('account_area/account_area.html')


@account_area.route('/change_password', methods=['POST'])
@login_required
def change_password():
    form_data = request.form
    current_password = form_data.get('current-password', None)
    new_password = form_data.get('new-password', None)
    confirm_password = form_data.get('confirm-password', None)

    error = ''
    if not (current_password and new_password and confirm_password):
        error = 'Please specify all fields'
    if not current_user.password == current_password:
        error = 'Current password incorrect'
    if not new_password == confirm_password:
        error = 'Password confirmation doesn\'t match'

    if error:
        return render_template('account_area/account_area.html', error=error)
    else:
        User.query.filter_by(id=current_user.id).update({
            'password': new_password
        })
        db.session.commit()
        return render_template('account_area/account_area.html')


@account_area.route('/change_email', methods=['POST'])
@login_required
def change_email():
    form_data = request.form
    new_email = form_data.get('email', None)

    error = ''
    if not new_email:
        error = 'Please specify an email'

    if error:
        return render_template('account_area/account_area.html', error=error)
    else:
        User.query.filter_by(id=current_user.id).update({
            'email': new_email
        })
        db.session.commit()
        return render_template('account_area/account_area.html')


@account_area.route('/send_feedback', methods=['POST'])
@login_required
def send_feedback():
    form_data = request.form
    print(request.form)
    feedback = form_data.get('feedback', None)

    error = ''
    if not feedback:
        error = 'Please specify feedback to send'

    if error:
        return render_template('account_area/account_area.html', error=error)
    else:
        new_message = Message(message=feedback, from_user=current_user.username)
        db.session.add(new_message)
        db.session.commit()
        return render_template('account_area/account_area.html')
