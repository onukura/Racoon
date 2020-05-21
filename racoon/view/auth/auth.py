# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, flash, abort, request, redirect, url_for
from flask_login import login_user, logout_user, current_user

from racoon.extensions import db, login_manager
from racoon.models.user import User, Roles
from racoon.view.auth.forms import LoginForm, RegistrationForm


bp_auth = Blueprint("bp_auth", __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@bp_auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("bp_home.home", _external=True))
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
        return redirect(url_for("bp_home.home", _external=True))
    return render_template("auth/login.html", form=form)


@bp_auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("bp_home.home", _external=True))


@bp_auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("bp_home.home", _external=True))
    form = RegistrationForm()
    if form.validate_on_submit():
        form.validate_email(form.email)
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.roles.append(Roles.query.filter(Roles.name == "member").first())
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("bp_auth.login"))
    return render_template("auth/register.html", form=form)
