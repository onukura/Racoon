from hashlib import md5
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from racoon.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    username = db.Column(db.String, unique=True)
    password_hash = db.Column(db.String(128))
    group_id = db.Column(db.Integer, nullable=True, default=0)

    def get_id(self):
        return self.user_id

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return "https://www.gravatar.com/avatar/{}?d=identicon&s={}".format(
            digest, size
        )


class Group(db.Model):
    __tablename__ = "group"
    group_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String, nullable=False)
