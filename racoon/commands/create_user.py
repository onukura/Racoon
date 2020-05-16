# -*- coding: utf-8 -*-
from flask_script import Command

from racoon.extensions import db
from racoon.models.user import User, Roles


class CreateUserCommand(Command):
    """ Initialize the database."""

    def run(self):
        create_user()


def create_user():
    if User.query.all():
        create = input("A user already exists! Create another? (y/n):")
        if create == "n":
            return
    username = input("Enter username: ")
    email = input("Enter email address: ")
    password = input("Password: ")
    assert password == input("Password (again): ")
    role_name = input("Role: ")
    role = Roles.query.filter(Roles.name == role_name).first()
    user = User(email=email, username=username, group_id=0)
    user.set_password(password)
    user.roles.append(role)
    db.session.add(user)
    db.session.commit()
    print("New user added.")
