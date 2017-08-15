from flask import Blueprint, session, request, url_for, redirect

xss_protection = Blueprint('xss_protection', __name__)


@xss_protection.route('/')
def index():
    xss_protection_enabled = session.get('xss_protection_enabled', False)
    session['xss_protection_enabled'] = not xss_protection_enabled

    next = request.args.get('next', url_for('index'))
    return redirect(next)
