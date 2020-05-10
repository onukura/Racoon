# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from flask_login import current_user


bp_compete = Blueprint("bp_compete", __name__)


@bp_compete.route("/compete")
def compete():
    return render_template("compete.html", user=current_user)
