# -*- coding: utf-8 -*-
from flask import Blueprint, render_template

from racoon.view.auth.utils import login_or_role_erquired


bp_user = Blueprint("bp_user", __name__)


@bp_user.route("/profile/<string:username>/")
@login_or_role_erquired(role_name=None)
def home(username):
    # get current competes
    # get current activity
    return render_template("user/home.html")


@bp_user.route("/profile/<string:username>/competes")
@login_or_role_erquired(role_name=None)
def competes(username):
    # get current competes
    # get current activity
    return render_template("user/competes.html")


@bp_user.route("/profile/<string:username>/datasets")
@login_or_role_erquired(role_name=None)
def datasets(username):
    # get current competes
    # get current activity
    return render_template("user/datasets.html")


@bp_user.route("/profile/<string:username>/notebooks")
@login_or_role_erquired(role_name=None)
def notebooks(username):
    # get current competes
    # get current activity
    return render_template("user/notebooks.html")


@bp_user.route("/profile/<string:username>/discussion")
@login_or_role_erquired(role_name=None)
def discussion(username):
    # get current competes
    # get current activity
    return render_template("user/discussion.html")


@bp_user.route("/profile/<string:username>/edit")
@login_or_role_erquired(role_name=None)
def edit(username):
    # get current competes
    # get current activity
    return render_template("user/edit.html")
