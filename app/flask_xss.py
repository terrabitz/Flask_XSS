from copy import deepcopy

from flask import Flask, render_template, g
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from utils import snake_to_title
from views.admin import admin
from views.decorators import remove_xss_protection
from views.sandboxes import (
    unsafe_params,
    unsafe_cookies
)

from app.login import load_user

NO_PROTECTION_PREFIX = '/no_protec'

login_manager = LoginManager()
app = Flask(__name__)

app.config['SECRET_KEY'] = 'Keep it secret, keep it safe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

db = SQLAlchemy(app)

login_manager.init_app(app)
login_manager.user_loader(load_user)

sandbox_paths = {
    unsafe_params: "/unsafe_params",
    unsafe_cookies: "/unsafe_cookies"
}

# Register all browser-protected blueprints
for blueprint, path in sandbox_paths.items():
    app.register_blueprint(blueprint, url_prefix=path)

# Create unprotected versions of each blueprint
unsafe_sandbox_paths = {}
for blueprint, path in sandbox_paths.items():
    blueprint_copy = deepcopy(blueprint)
    blueprint_copy.name += "_no_protection"
    blueprint_copy.after_request(remove_xss_protection)
    blueprint_copy_path = NO_PROTECTION_PREFIX + path
    app.register_blueprint(blueprint_copy, url_prefix=blueprint_copy_path)
    unsafe_sandbox_paths[blueprint_copy] = blueprint_copy_path

sandbox_paths.update(unsafe_sandbox_paths)

app.register_blueprint(admin, url_prefix='/admin')


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
def index():
    """Create an index of all available sandboxes"""
    pages = {snake_to_title(bp.name): path for bp, path in sandbox_paths.items()}
    return render_template('index.html', pages=pages, enumerate=enumerate, len=len)


if __name__ == '__main__':
    app.run()
