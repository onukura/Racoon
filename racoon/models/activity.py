# -*- coding: utf-8 -*-
import datetime
from racoon.extensions import db


class Activity(db.Model):
    __tablename__ = "activity"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    content = db.Column(db.String, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
