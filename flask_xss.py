from flask import Flask, render_template, request, send_from_directory, url_for
from copy import deepcopy

from utils import snake_to_title
from views import (
    unsafe_params,
    unsafe_cookies,
    remove_xss_protection
)

NO_PROTECTION_PREFIX = '/no_protec'

app = Flask(__name__)

blueprint_paths = {
    unsafe_params: "/unsafe_params",
    unsafe_cookies: "/unsafe_cookies"
}

# Register all browser-protected blueprints
for blueprint, path in blueprint_paths.items():
    app.register_blueprint(blueprint, url_prefix=path)

# Create unprotected versions of each blueprint
for blueprint, path in blueprint_paths.items():
    blueprint_copy = deepcopy(blueprint)
    blueprint_copy.name += "_no_protection"
    blueprint_copy.after_request(remove_xss_protection)
    app.register_blueprint(blueprint_copy, url_prefix=NO_PROTECTION_PREFIX + path)


@app.route('/')
def index():
    """Create an index of all available sandboxes"""
    pages = {snake_to_title(bp): url_for(bp + '.index') for bp in app.blueprints.keys()}
    return render_template('index.html', pages=pages, enumerate=enumerate, len=len)


if __name__ == '__main__':
    app.run()
