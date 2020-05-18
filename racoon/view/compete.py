# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user

from racoon.view.auth.utils import login_or_role_erquired

bp_compete = Blueprint("bp_compete", __name__, url_prefix="/compete")


@bp_compete.route("/")
@login_or_role_erquired("member")
def compete():
    return render_template("compete.html", user=current_user)


@bp_compete.route("/create", methods=["GET", "POST"])
@login_or_role_erquired("creator")
def create():
    if request.method == "GET":
        return render_template("compete_create.html")
    else:
        data = request.form.data
        return redirect(url_for("compete"))