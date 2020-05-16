# -*- coding: utf-8 -*-
from flask_script import Command

from racoon.extensions import db
from racoon.models.user import User, Roles, UserGroup


class InitDbCommand(Command):
    """ Initialize the database."""

    def run(self):
        init_db()
        print("Database has been initialized.")


def init_db():
    """ Initialize the database."""
    db.drop_all()
    db.create_all()
    create_users()


def create_users():
    """ Create admin users """
    # Adding roles
    admin_role = find_or_create_role("admin", "Admin")
    manager_role = find_or_create_role("manager", "Manager")
    creator_role = find_or_create_role("creator", "Creator")
    member_role = find_or_create_role("member", "Member")
    guest_role = find_or_create_role("guest", "Guest")
    # Add Groups
    create_default_groups()
    # Add admin users
    _ = find_or_create_user("admin@example.com", "admin", admin_role)


def find_or_create_role(name, label):
    """ Find existing role or create new role """
    role = Roles.query.filter(Roles.name == name).first()
    if not role:
        role = Roles(name=name, label=label)
        db.session.add(role)
        db.session.commit()
    return role


def find_or_create_user(email, username, role=None):
    """ Find existing user or create new user """
    user = User.query.filter(User.email == email).first()
    if not user:
        user = User(email=email, username=username)
        user.set_password("admin")
        if role:
            user.roles.append(role)
        db.session.add(user)
        db.session.commit()
    return user


def create_default_groups():
    group = UserGroup(name="public")
    db.session.add(group)
    db.session.commit()
