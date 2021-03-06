# -*- coding: utf-8 -*-
from flask import Blueprint, render_template


bp_error = Blueprint("bp_error", __name__, url_prefix="/error")


# Specific Error Handlers
@bp_error.route("/default")
def default():
    return render_template(
        "error/error_base.html",
        error_code=500,
        header_name="Error",
        error_message="We will work on fixing that right away.",
    )


@bp_error.route("/unauthorized")
def unauthorized():
    return render_template(
        "error/error_base.html",
        error_code=500,
        header_name="Unauthorized",
        error_message="Not allowed to access this contents.",
    )
