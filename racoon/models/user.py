import datetime
from hashlib import md5
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from racoon.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    username = db.Column(db.String, unique=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('user_role.id'), default=0)
    group_id = db.Column(db.Integer, db.ForeignKey('user_group.id'), default=0)
    last_seen = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    from_ = db.Column(db.DateTime, default=datetime.datetime.utcnow())

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


class UserRole(db.Model):
    __tablename__ = "user_role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)


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


class TeamMember(db.Model):
    __tablename__ = "team_member"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    team_id = db.Column(db.Integer, db.ForeignKey("user_team.id"))
    from_ = db.Column(db.DateTime, default=datetime.datetime.utcnow())
