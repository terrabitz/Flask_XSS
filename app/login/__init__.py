class User:
    def __init__(self):
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        return "1"


admin_user = User()


def load_user(user_id):
    return admin_user
