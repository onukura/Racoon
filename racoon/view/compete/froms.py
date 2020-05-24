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
    description_overview = StringField(
        "compete_description_overview",
        render_kw={"class": "form-control", "placeholder": "Description for overview"},
        widget=TextArea(),
    )
    description_eval = StringField(
        "compete_description_eval",
        render_kw={
            "class": "form-control",
            "placeholder": "Description for evaluation",
        },
        widget=TextArea(),
    )
    description_data = StringField(
        "compete_description_data",
        render_kw={"class": "form-control", "placeholder": "Description for data"},
        widget=TextArea(),
    )
    metric_type = RadioField(
        "compete_metric_type",
        validators=[DataRequired()],
        choices=[("regression", "Regression"), ("classification", "Classification")],
        default="regression",
        render_kw={"class": "form-check"},
    )
    metric_name = SelectField(
        "compete_metric_name", render_kw={"class": "form-control", "id": "metric_name"},
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
        format="%Y-%m-%d",
        validators=[Optional()],
        render_kw={"class": "form-control float-right"},
    )
    access_level = SelectField(
        "access_level",
        choices=[("1", "Public"), ("2", "Group"), ("3", "Private")],
        render_kw={"class": "form-control", "id": "access_level"},
    )


class SubmissionForm(FlaskForm):
    description = StringField(
        "description_submission",
        render_kw={"class": "form-control", "placeholder": "Description for overview"},
        widget=TextArea(),
    )
    file_prediction = FileField(
        validators=[
            FileRequired(),
            FileAllowed(ALLOWED_ANSWER_EXT, "csv&tsv&txt only!"),
        ],
        render_kw={"class": "custom-file-input"},
    )
