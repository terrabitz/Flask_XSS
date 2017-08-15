from flask import Flask, render_template, g, session, request
from flask_login import LoginManager, current_user
from flask_admin import Admin

from app.utils import snake_to_title, load_user
from app.blueprints.admin.views import AdminOnlyModelView, MessagesView
# from app.blueprints.admin.views import admin
from app.blueprints.login.views import authentication
from app.blueprints.xss_protection.views import xss_protection
from app.blueprints.api.views import api
from app.blueprints.sandboxes.views import (
    unsafe_params,
    unsafe_cookies
)
from app.models import (
    User,
    Message,
    db
)

app = Flask(__name__)

sandbox_paths = {
    unsafe_params: "/unsafe_params",
    unsafe_cookies: "/unsafe_cookies"
}


def config_app(app):
    app.config['SECRET_KEY'] = 'Keep it secret, keep it safe'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    app.config['EXPLAIN_TEMPLATE_LOADING'] = True
    app.config['DEBUG'] = True


def add_jinja_functions(app):
    """Adds desired python functions to be accessible from Jinja templates"""
    app.jinja_env.globals.update(
        hasattr=hasattr,
        enumerate=enumerate,
        len=len
    )


def init_extensions(app):
    """Initialize all 3rd party extensions here"""
    # Flask_SQLAlchemy
    db.init_app(app)

    # Flask_Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.user_loader(load_user)

    # Flask_Admin
    admin_interface = Admin(app, name='Flask XSS', template_mode='bootstrap3')
    admin_interface.add_view(AdminOnlyModelView(User, db.session))
    admin_interface.add_view(MessagesView(name='Messages', endpoint='messages'))


def register_blueprints(app):
    for blueprint, path in sandbox_paths.items():
        app.register_blueprint(blueprint, url_prefix=path)

    # app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(authentication, url_prefix='/auth')
    app.register_blueprint(xss_protection, url_prefix='/toggle_xss_protection')
    app.register_blueprint(api, url_prefix='/api/v1')


@app.before_request
def before_request():
    g.user = current_user
    g.session = session
    g.path = request.path


@app.after_request
def after_request(response):
    xss_protection_enabled = session.get('xss_protection_enabled', False)
    if not xss_protection_enabled:
        response.headers['X-XSS-Protection'] = 0

    return response


@app.route('/')
def index():
    """Create an index of all available sandboxes"""
    pages = {snake_to_title(bp.name): path for bp, path in sandbox_paths.items()}
    return render_template('index.html', pages=pages)


config_app(app)
add_jinja_functions(app)
init_extensions(app)
register_blueprints(app)

if __name__ == '__main__':
    app.run()
