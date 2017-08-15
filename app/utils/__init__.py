from app.models import User


def snake_to_title(string):
    return ' '.join([word.capitalize() for word in string.split('_')])


def load_user(user_id):
    return User.query.filter_by(id=user_id).first()
