from flask_login import UserMixin

from .db import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(200))
    email = db.Column(db.String(50))

    def __init__(self, username, password, email=""):
        self.username = username
        self.password = password
        self.email = email

    @property
    def is_admin(self):
        return self.username == "admin"


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(1000))

    def __init__(self, message):
        self.message = message
