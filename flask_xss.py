from flask import Flask, render_template, request, send_from_directory, url_for

from utils import snake_to_title
from views import (
    unsafe_params,
    unsafe_params_no_protection,
)


NO_PROTECTION_PREFIX = '/no_protec'

app = Flask(__name__)

app.register_blueprint(unsafe_params_no_protection, url_prefix=NO_PROTECTION_PREFIX + '/unsafe_params')
app.register_blueprint(unsafe_params, url_prefix='/unsafe_params')


@app.route('/')
def index():
    pages = {snake_to_title(bp): url_for(bp + '.index') for bp in app.blueprints.keys()}
    return render_template('index.html', pages=pages)


if __name__ == '__main__':
    app.run()
