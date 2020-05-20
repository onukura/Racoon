# -*- coding: utf-8 -*-
import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user

from racoon.lib.utils import clean_str
from racoon.view.auth.utils import login_or_role_erquired
from racoon.view.compete.froms import CreateCompetitionForm
from racoon.models.competition import Competition
from racoon.models.user import User
from racoon.extensions import db, storage


bp_compete = Blueprint("bp_compete", __name__, url_prefix="/compete")


@bp_compete.route("/")
@login_or_role_erquired("member")
def compete():
    return render_template("compete.html", user=current_user)


@bp_compete.route("/create", methods=["GET", "POST"])
@login_or_role_erquired("creator")
def create():
    form = CreateCompetitionForm()
    if request.method == "GET":
        return render_template("compete_create.html", form=form)
    else:
        form.metric.choices = [(form.metric.data, form.metric.data)]
        if form.validate_on_submit():
            # TODO
            user = User.query.filter(User.username == current_user.username).first()
            compete_name = clean_str(form.name)
            # Add competition record to db
            compete = Competition(
                name = compete_name,
                friendly_name = form.name,
                description = form.description,
                creator_id = user.id,
                access_level= form.access_level,
                created_date = datetime.datetime.now(),
                deadline_date = form.expired_date,
                is_open = True
            )
            db.session.add(compete)
            db.session.commit()
            # Create bucket
            storage.connection.make_bucket()

            data = form.file_data
            return redirect(url_for("bp_compete.compete", _external=True))
        else:
            return render_template("compete_create.html", form=form)
