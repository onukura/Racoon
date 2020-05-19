# -*- coding: utf-8 -*-
import datetime
from flask import Blueprint, render_template
from sqlalchemy import desc

from racoon.extensions import db
from racoon.models.user import User
from racoon.models.activity import Activity


bp_home = Blueprint("bp_home", __name__)


@bp_home.route("/")
@bp_home.route("/home")
def home():
    activities = (
        db.session.query(Activity, User)
        .outerjoin(User, Activity.user_id == User.id)
        .order_by(desc(Activity.date))
        .limit(20)
    )
    now = datetime.datetime.now().strftime("%Y-%m-%d")
    return render_template("home.html", now=now, activities=activities)
