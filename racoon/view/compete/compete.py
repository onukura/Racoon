# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user

from racoon.view.auth.utils import login_or_role_erquired
from racoon.view.compete.froms import CreateCompetitionForm


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
            #TODO
            data = form.file_data
            return redirect(url_for("bp_compete.compete", _external=True))
        else:
            return render_template("compete_create.html", form=form)
