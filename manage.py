from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, prompt_bool, Server

from app.flask_xss import app, db, User

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server())


@manager.command
def add_admin(password='admin'):
    """Create an admin user"""
    def create_and_add_admin():
        print('Adding new admin user')
        admin_user = User(username='admin', password=password)
        db.session.add(admin_user)
        db.session.commit()
        print('New admin credentials are admin/{}'.format(password))

    with app.app_context():
        admin_user = User.query.filter_by(username='admin').first()
        if admin_user:
            if prompt_bool('Admin user already exists. Override?'):
                db.session.delete(admin_user)
                db.session.commit()
                create_and_add_admin()
            else:
                print('Exiting...')
                exit(0)
        else:
            create_and_add_admin()


if __name__ == '__main__':
    manager.run()
