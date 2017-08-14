from distutils.core import setup

from app.flask_xss import app, db, User

with app.app_context():
    db.create_all()
    admin_user = User.query.filter_by(username='admin').first()
    print(admin_user)
    if not admin_user:
        admin_user = User(username="admin", password="admin")
        db.session.add(admin_user)
        db.session.commit()

setup(
    name='Flask XSS',
    version='1.0',
    description='A Flask XSS sandbox',
    author='Trevor Taubitz',
    author_email='trevor.taubitz@gmail.com',
    url='https://github.com/terrabitz/Flask_XSS',
)
