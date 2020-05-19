import datetime
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from racoon.extensions import db


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    username = db.Column(db.String, unique=True)
    password_hash = db.Column(db.String(128))
    group_id = db.Column(db.Integer, db.ForeignKey("user_group.id"), default=1)
    last_seen = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    from_ = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    # Relationships
    roles = db.relationship(
        "Roles", secondary="users_roles", backref=db.backref("user", lazy="dynamic")
    )

    def get_id(self):
        return self.id

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return "https://www.gravatar.com/avatar/{}?d=identicon&s={}".format(
            digest, size
        )


# Define the Role data model
class Roles(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String, nullable=False, server_default="", unique=True
    )  # for @roles_accepted()
    label = db.Column(db.Unicode(255), server_default="")  # for display purposes


# Define the UserRoles association model
class UsersRoles(db.Model):
    __tablename__ = "users_roles"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id", ondelete="CASCADE"))


class UserGroup(db.Model):
    __tablename__ = "user_group"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    from_ = db.Column(db.DateTime, default=datetime.datetime.utcnow())


class UserTeam(db.Model):
    __tablename__ = "user_team"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    from_ = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    is_active = db.Column(db.Boolean, default=True)


class UsersTeams(db.Model):
    __tablename__ = "users_teams"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    team_id = db.Column(db.Integer, db.ForeignKey("user_team.id"))
    from_ = db.Column(db.DateTime, default=datetime.datetime.utcnow())
