# -*- coding: utf-8 -*-
import datetime

from racoon.extensions import db


class Competition(db.Model):
    __tablename__ = "competition"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    friendly_name = db.Column(db.String, nullable=True)
    description_overview = db.Column(db.String, nullable=True)
    description_eval = db.Column(db.String, nullable=True)
    description_data = db.Column(db.String, nullable=True)
    creator_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    access_level = db.Column(db.Integer)  # 1:personal, 2:group, 3:public
    created_date = db.Column(db.DateTime, default=datetime.datetime.now())
    deadline_date = db.Column(db.DateTime, nullable=True)
    is_open = db.Column(db.Boolean, default=True, nullable=False)

    def is_user_joined(self, user_id):
        res = (
            CompetitionAttendee.query.filter(
                CompetitionAttendee.competition_id == self.id
            )
            .filter(CompetitionAttendee.user_id == user_id)
            .first()
        )
        if res:
            return True
        return False


class CompetitionAttendee(db.Model):
    __tablename__ = "competition_attendee"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    competition_id = db.Column(db.Integer, db.ForeignKey("competition.id"))
    attended_date = db.Column(db.DateTime, default=datetime.datetime.now())
    quit_date = db.Column(db.DateTime, default=None)
    is_active = db.Column(db.Boolean, default=True)


class CompetitionScore(db.Model):
    __tablename__ = "competition_score"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    competition_id = db.Column(db.Integer, db.ForeignKey("competition.id"))
    score = db.Column(db.Numeric, nullable=True)
    posted_date = db.Column(db.DateTime, default=datetime.datetime.now())


class CompetitionActivity(db.Model):
    __tablename__ = "competition_activity"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    competition_id = db.Column(db.Integer, db.ForeignKey("competition.id"))
    content = db.Column(db.String, nullable=False)
