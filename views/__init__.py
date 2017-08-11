from flask import request, render_template, Blueprint

unsafe_params_no_protection = Blueprint('unsafe_params_no_protection', __name__, )


@unsafe_params_no_protection.route('/')
def index():
    """Renders a page"""
    test = request.args.get('name', ' world!')
    return render_template('unsafe_params.html', test=test), 200


unsafe_params = Blueprint('unsafe_params', __name__)


@unsafe_params.route('/')
def index():
    """Renders a page with XSS flags enabled to use browser-based defenses"""
    test = request.args.get('name', ' world!')
    return render_template('unsafe_params.html', test=test), 200


@unsafe_params_no_protection.after_app_request
def remove_xss_protection(response):
    response.headers['X-XSS-Protection'] = 0
    return response
