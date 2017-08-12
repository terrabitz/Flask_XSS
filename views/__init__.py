from flask import request, render_template, Blueprint, current_app

unsafe_params = Blueprint('unsafe_params', __name__)


@unsafe_params.route('/')
def index():
    """Renders a page with XSS flags enabled to use browser-based defenses"""
    title = 'Unsafe Parameters'
    description = 'A GET parameter is unsafely handled. Try entering something in the text box, or setting ' \
                  '"?name=something" in the header'

    name = request.args.get('name', 'world!')
    return render_template('unsafe_params.html', name=name, title=title, description=description)


unsafe_cookies = Blueprint('unsafe_cookies', __name__)


@unsafe_cookies.route('/', methods=["GET", "POST"])
def index():
    """Renders a page that processes cookies in an unsafe way"""
    title = 'Unsafe Cookies'
    description = 'A cookie called "name" is unsafely handled. Try setting it using a cookie editor, or by enter a ' \
                  'new name in the text box below'

    cookie_name = request.cookies.get('name', 'world')
    new_name = request.form.get('name', None)
    if new_name:
        # Form was submitted, change  cookie
        name = new_name
    else:
        # Use previous cookie
        name = cookie_name

    response = current_app.make_response(
        render_template('unsafe_cookies.html', name=name, title=title, description=description))
    response.set_cookie('name', name)
    return response


def remove_xss_protection(response):
    response.headers['X-XSS-Protection'] = 0
    return response
