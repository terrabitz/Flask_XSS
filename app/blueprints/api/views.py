from flask import Blueprint, jsonify, request
from flask_classy import FlaskView, route

from app.models import Message, db
from app.blueprints.decorators import admin_required

API_STATUS_SUCCESS = {'status': 'success'}
API_STATUS_ERROR = {'status': 'error'}

api = Blueprint('api', __name__)


class MessagesView(FlaskView):
    @admin_required
    def index(self):
        messages = Message.query.all()
        messages_list = [message.serialize for message in messages]

        response = {'messages': messages_list}
        response.update(API_STATUS_SUCCESS)
        return jsonify(response)

    @admin_required
    def get(self, id):
        message = Message.query.filter_by(id=id).first().serialize
        if not message:
            return jsonify(API_STATUS_ERROR)

        response = {'message': message}
        response.update(API_STATUS_SUCCESS)
        return jsonify(response)

    @admin_required
    def delete(self, id):
        message = Message.query.filter_by(id=id).first()
        if not message:
            return jsonify(API_STATUS_ERROR)
        db.session.delete(message)
        db.session.commit()

        return jsonify(API_STATUS_SUCCESS)

    def post(self):
        data = request.get_json()
        if not data:
            return API_STATUS_ERROR
        message = data.get('message', None)
        if not message:
            return API_STATUS_ERROR
        from_user = data.get('from_user', 'Anonymous')

        new_message = Message(message=message, from_user=from_user)
        db.session.add(new_message)
        db.session.commit()

        return jsonify(API_STATUS_SUCCESS)

    @route('/acknowledge/<id>', methods=['POST'])
    @admin_required
    def acknowledge_message(self, id):
        Message.query.filter_by(id=id).update({
            'acknowledged': True
        })
        db.session.commit()

        return jsonify(API_STATUS_SUCCESS)


MessagesView.register(api)
