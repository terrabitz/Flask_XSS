from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)


@app.route('/')
def hello_world():
    test = request.args.get('name', ' world!')
    return render_template('index.html', test=test), 200, {'X-XSS-Protection': 0}

# @app.route('/static/<path:file>')
# def static(file):
#     return send_from_directory('static', file)

if __name__ == '__main__':
    app.run()
