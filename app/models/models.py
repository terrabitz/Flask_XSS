from flask_login import UserMixin

from .db import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(200))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @property
    def is_admin(self):
        return self.username == "admin"


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(1000))

    def __init__(self, message):
        self.message = message


def load_user(user_id):
    return User.query.filter_by(id=user_id).first()
