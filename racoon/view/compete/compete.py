# -*- coding: utf-8 -*-
import sys
import datetime

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from werkzeug.utils import secure_filename

from racoon.lib.utils import clean_str
from racoon.view.auth.utils import login_or_role_erquired
from racoon.view.compete.froms import CreateCompetitionForm
from racoon.models.competition import Competition
from racoon.models.user import User
from racoon.extensions import db, storage


bp_compete = Blueprint("bp_compete", __name__, url_prefix="/compete")


@bp_compete.route("/")
@login_or_role_erquired("member")
def list():
    return render_template("compete/list.html", user=current_user)


@bp_compete.route("/create", methods=["GET", "POST"])
@login_or_role_erquired("creator")
def create():
    form = CreateCompetitionForm()
    if request.method == "GET":
        return render_template("compete/create.html", form=form)
    else:
        form.metric.choices = [(form.metric.data, form.metric.data)]
        if form.validate_on_submit():
            # TODO
            compete_name = clean_str(form.name.data)
            # Add competition record to db
            compete = Competition(
                name = compete_name,
                friendly_name = form.name.data,
                description = form.description.data,
                creator_id = current_user.id,
                access_level= int(form.access_level.data),
                created_date = datetime.datetime.now(),
                deadline_date = form.expired_date.data,
                is_open = True
            )
            db.session.add(compete)
            db.session.commit()
            # Create bucket
            storage.connection.make_bucket(compete_name)
            # Data upload to bucket
            file_answer = form.file_answer.data
            filename = secure_filename(file_answer.filename)
            storage.connection.put_object(compete_name, filename, file_answer, length=sys.getsizeof(file_answer), content_type='application/csv')
            return redirect(url_for("bp_compete.list", _external=True))
        else:
            return render_template("compete/create.html", form=form)


@bp_compete.route("/<string:compete_name>/overview")
@login_or_role_erquired("member")
def detail():
    return render_template("compete/overview.html")