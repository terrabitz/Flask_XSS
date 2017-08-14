from .db import db

class User:
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(200))

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Message:
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(1000))

    def __init__(self, message):
        self.message = message
