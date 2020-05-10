# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError

from racoon.models.user import User


class LoginForm(FlaskForm):
    username = StringField(
        "username",
        validators=[DataRequired()],
        render_kw={"class": "form-control", "placeholder": "Username"},
    )
    password = PasswordField(
        "password",
        validators=[DataRequired()],
        render_kw={"class": "form-control", "placeholder": "Password"},
    )
    remember_me = BooleanField("Remember Me")


class RegistrationForm(FlaskForm):
    username = StringField(
        "username",
        validators=[DataRequired()],
        render_kw={"class": "form-control", "placeholder": "Username"},
    )
    email = StringField(
        "email",
        validators=[DataRequired(), Email()],
        render_kw={"class": "form-control", "placeholder": "E-mail"},
    )
    password = PasswordField(
        "password",
        validators=[DataRequired()],
        render_kw={"class": "form-control", "placeholder": "Password"},
    )
    password2 = PasswordField(
        "repeat password",
        validators=[DataRequired(), EqualTo("password")],
        render_kw={"class": "form-control", "placeholder": "Repeat password"},
    )

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address.")
