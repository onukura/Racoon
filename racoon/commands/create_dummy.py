# -*- coding: utf-8 -*-
import datetime

from flask_script import Command

from racoon.extensions import db
from racoon.models.user import User, Roles
from racoon.models.activity import GeneralActivity


class CreateDummyData(Command):
    """ Create dummy data for test."""

    def run(self):
        create_dummy_data()


def create_dummy_data():
    create_dummy_user()
    create_dummy_activity()
    print("dummy date created.")


def generate_user(email, username, password, role_name):
    role = Roles.query.filter(Roles.name == role_name).first()
    assert role is not None
    user = User(email=email, username=username)
    user.set_password(password)
    user.roles.append(role)
    return user


def create_dummy_user():
    user_list = [
        generate_user(
            email="hoge1@hoge1.com",
            username="hoge1",
            password="hoge1",
            role_name="member",
        ),
        generate_user(
            email="hoge1@hoge2.com",
            username="hoge2",
            password="hoge2",
            role_name="member",
        ),
    ]
    db.session.add_all(user_list)
    db.session.commit()


def create_dummy_activity():
    db.session.add_all(
        [
            GeneralActivity(
                id=i,
                date=datetime.datetime(2020, 5, 1, i, 10, 10),
                content=f"activity_{i}",
                user_id=int(i % 3 + 1),
            )
            for i in range(24)
        ]
    )
    db.session.commit()
