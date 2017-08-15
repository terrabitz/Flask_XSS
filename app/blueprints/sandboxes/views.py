from flask import Blueprint, request, render_template, current_app

sandboxes = Blueprint('sandboxes', __name__, template_folder='templates')


@sandboxes.route('/unsafe_params')
def unsafe_params():
    """Renders a page with XSS flags enabled to use browser-based defenses"""
    title = 'Unsafe Parameters'
    description = 'A GET parameter is unsafely handled. Try entering something in the text box, or setting ' \
                  '"?name=something" in the header'

    name = request.args.get('name', 'world!')
    return render_template('sandboxes/unsafe_params.html', name=name, title=title, description=description)


unsafe_cookies = Blueprint('unsafe_cookies', __name__)


@sandboxes.route('/unsafe_cookies', methods=["GET", "POST"])
def unsafe_cookies():
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
        render_template('sandboxes/unsafe_cookies.html', name=name, title=title, description=description))
    response.set_cookie('name', name)
    return response
