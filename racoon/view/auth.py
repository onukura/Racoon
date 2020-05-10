# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, flash, abort, request, redirect, url_for
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

from racoon.models.user import User

bp_auth = Blueprint("bp_auth", __name__)


class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])


@bp_auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("bp_index.index", _external=True))
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("bp_index.index", _external=True))

    return render_template("login.html", title="Sign In", form=form)


@bp_auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('bp_index.index', _external=True))


@bp_auth.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")


def is_safe_url(next):
    # TODO implement is_url_safe http://flask.pocoo.org/snippets/62/
    return True
