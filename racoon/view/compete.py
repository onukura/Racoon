# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from flask_login import current_user, login_required

from racoon.view.auth.utils import login_or_role_erquired

bp_compete = Blueprint("bp_compete", __name__)


@bp_compete.route("/compete")
@login_or_role_erquired("member")
def compete():
    return render_template("compete.html", user=current_user)
