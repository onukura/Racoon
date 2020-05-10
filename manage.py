"""This file is the view module which contains the lazysensor, where all the good
stuff happens. You will always want to point your applications like Gunicorn
to this file, which will pick up the lazysensor to run their servers.
"""

import os

from flask_script import Manager

from racoon import create_app
from racoon.extensions import db
from racoon.models.user import User

try:
    FLASK_CONFIG = os.environ["DEBUG"]
except:
    FLASK_CONFIG = "debug"

# Generate Flask App
app = create_app(FLASK_CONFIG)

manager = Manager(app)


@manager.command
def create_user():
    with app.app_context():
        if User.query.all():
            create = input("A user already exists! Create another? (y/n):")
            if create == "n":
                return
        username = input("Enter username: ")
        email = input("Enter email address: ")
        password = input("Password: ")
        assert password == input("Password (again): ")

        user = User(email=email, username=username, group_id=0)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print("User added.")


@manager.command
def create_admin():
    with app.app_context():
        user = User(email="admin@admin.org", username="admin")
        user.set_password("admin")
        db.session.add(user)
        db.session.commit()
        print("Admin user added.")


@manager.command
def initialize_db():
    """
    Recreates a local database. You probably should not use this on
    production.
    """
    with app.app_context():
        app.logger.info("start recreate_db.")
        db.drop_all()
        app.logger.info("dropped all tables.")
        db.create_all()
        app.logger.info("recreated all tables.")
        db.session.commit()
        app.logger.info("recreate_db done")
    print("Database initialized.")


if __name__ == "__main__":
    # Import HTTP server module and run API
    manager.run()
