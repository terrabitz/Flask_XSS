from flask import Blueprint, jsonify, request
from flask_classy import FlaskView, route

from app.models import Message, User, db
from app.blueprints.decorators import admin_required, is_admin_or_owning_user

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


class UsersView(FlaskView):
    @admin_required
    def index(self):
        users = [user.serialize for user in User.query.all()]
        ret = {'users': users}
        ret.update(API_STATUS_SUCCESS)
        return jsonify(ret)

    def get(self, id):
        if not is_admin_or_owning_user(id):
            return jsonify(API_STATUS_ERROR)

        user = User.query.filter_by(id=id).first()
        if not user:
            return jsonify(API_STATUS_ERROR)
        ret = {'user': user}
        ret.update(API_STATUS_SUCCESS)
        return jsonify(ret)

    @admin_required
    def post(self):
        data = request.get_json()
        if not data:
            return jsonify(API_STATUS_ERROR)
        username = data.get('username', None)
        if not username:
            return jsonify(API_STATUS_ERROR)


    def put(self, id):
        if not is_admin_or_owning_user(id):
            return jsonify(API_STATUS_ERROR)



MessagesView.register(api)
