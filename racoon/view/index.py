# -*- coding: utf-8 -*-
from flask import Blueprint, render_template

bp_index = Blueprint("bp_index", __name__)


@bp_index.route("/")
def index():
    return render_template("index.html")
