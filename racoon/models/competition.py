# -*- coding: utf-8 -*-
import datetime
from racoon.extensions import db


class Competition(db.Model):
    __tablename__ = "competition"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String, nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    create_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    access_level = db.Column(db.Integer)  # 1:personal, 2:group, 3:public
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    deadline_date = db.Column(db.DateTime, nullable=True)
    is_open = db.Column(db.Boolean, default=True, nullable=False)


class CompetitionAttendee(db.Model):
    __tablename__ = "competition_attendee"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    competition_id = db.Column(db.Integer, db.ForeignKey("competition.id"))
    attended_date = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    quit_date = db.Column(db.DateTime, default=None)
    is_active = db.Column(db.Boolean, default=True)


class CompetitionScore(db.Model):
    __tablename__ = "competition_score"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    competition_id = db.Column(db.Integer, db.ForeignKey("competition.id"))
    score = db.Column(db.Numeric, nullable=True)
    posted_date = db.Column(db.DateTime, default=datetime.datetime.utcnow())
