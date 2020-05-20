# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SelectField, RadioField, DateField
from wtforms.validators import DataRequired, Optional
from wtforms.widgets import TextArea


ALLOWED_ANSWER_EXT = ["csv", "tsv", "txt"]


class CreateCompetitionForm(FlaskForm):
    name = StringField(
        "compete_name",
        validators=[DataRequired()],
        render_kw={"class": "form-control", "placeholder": "Competition Name"},
    )
    description = StringField(
        "compete_description",
        render_kw={"class": "form-control", "placeholder": "Description"},
        widget=TextArea(),
    )
    eval_type = RadioField(
        "compete_eval_type",
        validators=[DataRequired()],
        choices=[("regression", "Regression"), ("classification", "Classification")],
        default="regression",
        render_kw={"class": "form-check"},
    )
    metric = SelectField(
        "compete_metric", render_kw={"class": "form-control", "id": "metric"},
    )
    file_answer = FileField(
        validators=[
            FileRequired(),
            FileAllowed(ALLOWED_ANSWER_EXT, "csv&tsv&txt only!"),
        ],
        render_kw={"class": "custom-file-input"},
    )
    file_data = FileField(render_kw={"class": "custom-file-input"})
    expired_date = DateField(
        "expired_date",
        format="%m/%d/%Y",
        validators=[Optional()],
        render_kw={"class": "form-control float-right"},
    )
    access_level = SelectField(
        "access_level",
        choices=[(1, "Public"), (2, "Group"), (3, "Private")],
        render_kw={"class": "form-control", "id": "access_level"}
    )
