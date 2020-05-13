"""This file is the view module which contains the lazysensor, where all the good
stuff happens. You will always want to point your applications like Gunicorn
to this file, which will pick up the lazysensor to run their servers.
"""

import os

from flask_script import Manager

from racoon import create_app

try:
    FLASK_CONFIG = os.environ["FLASK_CONFIG"]
except:
    FLASK_CONFIG = "debug"

# Generate Flask App
app = create_app(FLASK_CONFIG)

manager = Manager(app)


@manager.command
def create_user():
    with app.app_context():
        from racoon.extensions import db
        from racoon.models.user import User
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
        from racoon.extensions import db
        from racoon.models.user import User
        user = User(email="admin@admin.org", username="admin", role_id=0)
        user.set_password("admin")
        db.session.add(user)
        db.session.commit()
    print("Admin user added.")


@manager.command
def init_user():
    with app.app_context():
        from racoon.extensions import db
        from racoon.models.user import UserGroup, UserRole
        db.session.add(UserGroup(id=0, name="public"))
        db.session.add_all([
            UserRole(id=0, name="admin"),
            UserRole(id=1, name="manager"),
            UserRole(id=2, name="guest"),
        ])
    create_admin()
    print("Tables for users initialized.")


@manager.command
def recreate_db():
    """
    Recreates a local database. You probably should not use this on
    production.
    """
    with app.app_context():
        from racoon.extensions import db
        app.logger.info("start recreate_db.")
        db.drop_all()
        app.logger.info("dropped all tables.")
        db.create_all()
        app.logger.info("recreated all tables.")
        db.session.commit()
        app.logger.info("recreate_db done")
    print("Database initialized.")


@manager.command
def init_app():
    recreate_db()
    init_user()


@manager.command
def create_dummy_data():
    with app.app_context():
        import datetime
        from racoon.extensions import db
        from racoon.models.user import User
        from racoon.models.activity import Activity
        # Add User
        user1 = User(email="hoge1@hoge1.org", username="hoge1", role_id=1)
        user1.set_password("hoge1")
        user2 = User(email="hoge2@hoge2.org", username="hoge2", role_id=2)
        user2.set_password("hoge2")
        db.session.add_all([user1, user2])
        db.session.commit()
        # Add activities
        db.session.add_all([
            Activity(id=i,
                     date=datetime.datetime(2020, 5, 1, i, 10, 10),
                     content=f"activity_{i}",
                     user_id=int(i % 3 + 1))
            for i in range(24)
        ])
        db.session.commit()
    print("dummy date created.")


if __name__ == "__main__":
    # Import HTTP server module and run API
    manager.run()
