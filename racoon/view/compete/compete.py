# -*- coding: utf-8 -*-
import datetime
import io
import os
import sys
import time
import zipfile
from io import BytesIO

import pandas as pd
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    current_app,
    make_response,
)
from flask_login import current_user
from werkzeug.utils import secure_filename

from racoon.extensions import db, storage
from racoon.lib.utils import clean_str
from racoon.lib.evals import Metric
from racoon.models.activity import GeneralActivity
from racoon.models.competition import (
    Competition,
    CompetitionAttendee,
    CompetitionActivity,
    CompetitionSubmission,
    CompetitionScore,
)
from racoon.view.auth.utils import login_or_role_erquired
from racoon.view.compete.froms import CreateCompetitionForm, SubmissionForm


bp_compete = Blueprint("bp_compete", __name__, url_prefix="/compete")


@bp_compete.route("/")
@login_or_role_erquired("member")
def list():
    competes = Competition.query.all()
    competes_private = []
    competes_public = []
    [
        competes_private.append(c)
        if c.is_user_joined(current_user.id)
        else competes_public.append(c)
        for c in competes
    ]
    return render_template(
        "compete/list.html",
        competes_private=competes_private,
        competes_public=competes_public,
    )


@bp_compete.route("/create", methods=["GET", "POST"])
@login_or_role_erquired("creator")
def create():
    form = CreateCompetitionForm()
    if request.method == "GET":
        return render_template("compete/create.html", form=form)
    else:
        form.metric_name.choices = [(form.metric_name.data, form.metric_name.data)]
        if form.validate_on_submit():
            compete_name = clean_str(form.name.data)
            # Add competition record to db
            compete = Competition(
                name=compete_name,
                friendly_name=form.name.data,
                description_overview=form.description_overview.data,
                description_eval=form.description_eval.data,
                description_data=form.description_data.data,
                metric_type=form.metric_type.data,
                metric_name=form.metric_name.data,
                creator_id=current_user.id,
                access_level=int(form.access_level.data),
                created_date=datetime.datetime.now(),
                deadline_date=form.expired_date.data,
                is_open=True,
            )
            db.session.add(compete)
            db.session.commit()
            # Add this user to attendee
            __compete = Competition.query.filter(
                Competition.name == compete_name
            ).first()
            attendee = CompetitionAttendee(
                user_id=current_user.id,
                competition_id=__compete.id,
                attended_date=datetime.datetime.now(),
            )
            db.session.add(attendee)
            db.session.commit()
            # Create bucket
            storage.connection.make_bucket(compete_name)
            # Answer data upload to bucket
            # TODO last row of csv is strangely empty.
            file_answer = form.file_answer.data
            filename_answer = current_app.config[
                "FILENAME_ANSWER"
            ]  # secure_filename(file_answer.filename)
            upload_dir_answer = current_app.config["STORAGE_PATH_ANSWER"]
            storage.connection.put_object(
                compete_name,
                f"{upload_dir_answer}/{filename_answer}",
                file_answer,
                length=sys.getsizeof(file_answer),
                content_type="application/csv",
            )
            # Etc data upload to bucket
            if form.file_data.data is not None:
                # etc. data is multiple file input
                for _file_data in form.file_data.data:
                    _filename_data = secure_filename(_file_data.filename)
                    upload_dir_data = current_app.config["STORAGE_PATH_DATA"]
                    storage.connection.put_object(
                        compete_name,
                        f"{upload_dir_data}/{_filename_data}",
                        _file_data,
                        length=sys.getsizeof(_file_data),
                        content_type="application/csv",
                    )
            # Add this event to CompetitionActivity
            compete_activity = CompetitionActivity(
                user_id=current_user.id,
                competition_id=__compete.id,
                content=f"Opened by {current_user.username}",
            )
            db.session.add(compete_activity)
            db.session.commit()
            # Add this event to GeneralActivity
            general_activity = GeneralActivity(
                date=datetime.datetime.now(),
                content=f"opened new competition '{form.name.data}'.",
                user_id=current_user.id,
            )
            db.session.add(general_activity)
            db.session.commit()
            return redirect(
                url_for(
                    "bp_compete.overview", compete_name=compete_name, _external=True
                )
            )
        else:
            return render_template("compete/create.html", form=form)


@bp_compete.route("/<string:compete_name>/overview")
@login_or_role_erquired("member")
def overview(compete_name):
    compete = Competition.query.filter(Competition.name == compete_name).first()
    is_joined = compete.is_user_joined(current_user.id)
    if compete:
        return render_template(
            "compete/overview.html", compete=compete, is_joined=is_joined
        )
    return redirect(url_for("bp_compete.list", _external=True))


@bp_compete.route("/<string:compete_name>/data")
@login_or_role_erquired("member")
def data(compete_name):
    upload_dir = current_app.config["STORAGE_PATH_DATA"]
    compete = Competition.query.filter(Competition.name == compete_name).first()
    data_list = storage.connection.list_objects_v2(
        compete_name, recursive=True, start_after=upload_dir
    )
    data_dict = [
        {
            "name": os.path.basename(i.object_name),
            "size": round(i.size / 1024, ndigits=2),
        }
        for i in data_list
    ]
    if compete:
        return render_template(
            "compete/data.html", compete=compete, data_dict=data_dict
        )


@bp_compete.route("/<string:compete_name>/data/download/<string:filename>")
@login_or_role_erquired("member")
def data_download(compete_name, filename):
    upload_dir = current_app.config["STORAGE_PATH_DATA"]
    file = storage.connection.get_object(compete_name, f"{upload_dir}/{filename}")
    fileobj = io.BytesIO()
    with zipfile.ZipFile(fileobj, "w") as zip_file:
        zip_info = zipfile.ZipInfo(filename)
        zip_info.date_time = time.localtime(time.time())[:6]
        zip_info.compress_type = zipfile.ZIP_DEFLATED
        zip_file.writestr(zip_info, file.data)
    fileobj.seek(0)
    response = make_response(fileobj.read())
    response.headers.set("Content-Type", "zip")
    response.headers.set(
        "Content-Disposition",
        "attachment",
        filename="%s.zip" % os.path.splitext(os.path.basename(filename))[0],
    )
    return response


@bp_compete.route("/<string:compete_name>/discussion")
@login_or_role_erquired("member")
def discussion(compete_name):
    return redirect(request.url)


@bp_compete.route("/<string:compete_name>/notebook")
@login_or_role_erquired("member")
def notebook(compete_name):
    return redirect(request.url)


@bp_compete.route("/<string:compete_name>/leaderboard")
@login_or_role_erquired("member")
def leaderboard(compete_name):
    compete = Competition.query.filter(Competition.name == compete_name).first()
    return redirect(request.url)


@bp_compete.route("/<string:compete_name>/join")
@login_or_role_erquired("member")
def join(compete_name):
    compete = Competition.query.filter(Competition.name == compete_name).first()
    attendee = CompetitionAttendee(
        user_id=current_user.id,
        competition_id=compete.id,
        attended_date=datetime.datetime.now(),
    )
    db.session.add(attendee)
    db.session.commit()
    return redirect(url_for("bp_compete.overview", compete_name=compete_name))


@bp_compete.route("/<string:compete_name>/mysubmission")
@login_or_role_erquired("member")
def mysubmission(compete_name):
    print(compete_name)
    return redirect(request.url)


@bp_compete.route("/<string:compete_name>/submission", methods=["GET", "POST"])
@login_or_role_erquired("member")
def submission(compete_name):
    compete = Competition.query.filter(Competition.name == compete_name).first()
    is_joined = compete.is_user_joined(current_user.id)
    form = SubmissionForm()
    if request.method == "GET":
        return render_template(
            "compete/submission.html", compete=compete, form=form, is_joined=is_joined
        )
    elif request.method == "POST":
        if form.validate_on_submit():
            # save uploaded file to storage
            file_submit = form.file_prediction.data
            filename = secure_filename(file_submit.filename)
            upload_dir = current_app.config["STORAGE_PATH_SUBMISSION"]
            storage.connection.put_object(
                compete_name,
                f"{upload_dir}/{current_user.id}/{filename}",
                file_submit,
                length=sys.getsizeof(file_submit),
                content_type="application/csv",
            )
            del file_submit
            # register submission to submission table
            submit_date = datetime.datetime.now()
            submit = CompetitionSubmission(
                user_id=current_user.id,
                competition_id=compete.id,
                submit_date=submit_date,
                file_name=filename,
                description=form.description.data,
            )
            db.session.add(submit)
            db.session.commit()
            # load files
            answer_dir = current_app.config["STORAGE_PATH_ANSWER"]
            filename_answer = current_app.config["FILENAME_ANSWER"]
            file_answer = storage.connection.get_object(
                bucket_name=compete_name, object_name=f"{answer_dir}/{filename_answer}"
            )
            file_submit = storage.connection.get_object(
                bucket_name=compete_name,
                object_name=f"{upload_dir}/{current_user.id}/{filename}",
            )
            # calculate metric
            df_answer = pd.read_csv(file_answer, header=None, names=['id', 'y'])
            df_submit = pd.read_csv(file_submit, header=None, names=['id', 'yhat'])
            metric = Metric(
                answer=df_answer,
                prediction=df_submit,
                metric_type=compete.metric_type,
                metric_name=compete.metric_name,
            )
            metric.check_prediction()
            _score = metric.calc_score()
            # register metric to score table
            submit = CompetitionSubmission.query. \
                filter(CompetitionSubmission.user_id==current_user.id). \
                filter(CompetitionSubmission.competition_id==compete.id). \
                filter(CompetitionSubmission.submit_date == submit_date). \
                first()
            score = CompetitionScore(
                user_id=current_user.id,
                competition_id=compete.id,
                submission_id=submit.id,
                score=_score
            )
            db.session.add(score)
            db.session.commit()
            redirect(url_for("bp_compete.leaderboard", compete_name=compete_name))
    return redirect(url_for("bp_compete.overview", compete_name=compete_name))
