# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from flask_login import current_user


bp_index = Blueprint("bp_index", __name__)


@bp_index.route("/")
@bp_index.route("/index")
def index():
    return render_template("index.html", user=current_user)
