# -*- coding: utf-8 -*-
import sys
import datetime
import time
import os
import io
import zipfile

from flask import Blueprint, render_template, request, redirect, url_for, current_app, make_response
from flask_login import current_user
from werkzeug.utils import secure_filename

from racoon.lib.utils import clean_str
from racoon.view.auth.utils import login_or_role_erquired
from racoon.view.compete.froms import CreateCompetitionForm
from racoon.models.competition import Competition
from racoon.models.activity import GeneralActivity
from racoon.extensions import db, storage


bp_compete = Blueprint("bp_compete", __name__, url_prefix="/compete")


@bp_compete.route("/")
@login_or_role_erquired("member")
def list():
    return render_template("compete/list.html", user=current_user)


@bp_compete.route("/create", methods=["GET", "POST"])
@login_or_role_erquired("creator")
def create():
    form = CreateCompetitionForm()
    if request.method == "GET":
        return render_template("compete/create.html", form=form)
    else:
        form.metric.choices = [(form.metric.data, form.metric.data)]
        if form.validate_on_submit():
            compete_name = clean_str(form.name.data)
            # Add competition record to db
            compete = Competition(
                name=compete_name,
                friendly_name=form.name.data,
                description_overview=form.description_overview.data,
                description_eval=form.description_eval.data,
                description_data=form.description_data.data,
                creator_id=current_user.id,
                access_level=int(form.access_level.data),
                created_date=datetime.datetime.now(),
                deadline_date=form.expired_date.data,
                is_open=True,
            )
            db.session.add(compete)
            db.session.commit()
            # Create bucket
            storage.connection.make_bucket(compete_name)
            # Data upload to bucket
            file_answer = form.file_answer.data
            filename = secure_filename(file_answer.filename)
            upload_dir = current_app.config["MINIO_UPLOAD_DATA_PATH"]
            storage.connection.put_object(
                compete_name,
                f"{upload_dir}/{filename}",
                file_answer,
                length=sys.getsizeof(file_answer),
                content_type="application/csv",
            )
            general_acivity = GeneralActivity(
                date=datetime.datetime.now(),
                content=f"opened new competition '{form.name.data}'.",
                user_id=current_user.id
            )
            db.session.add(general_acivity)
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
    if compete:
        return render_template("compete/overview.html", compete=compete)
    return redirect(url_for("bp_compete.list", _external=True))


@bp_compete.route("/<string:compete_name>/data")
@login_or_role_erquired("member")
def data(compete_name):
    upload_dir = current_app.config["MINIO_UPLOAD_DATA_PATH"]
    compete = Competition.query.filter(Competition.name == compete_name).first()
    data_list = storage.connection.list_objects_v2(compete_name, recursive=True, start_after=upload_dir)
    data_dict = [{"name": os.path.basename(i.object_name), "size": round(i.size / 1024, ndigits=2)} for i in data_list]
    if compete:
        return render_template("compete/data.html", compete=compete, data_dict=data_dict)


@bp_compete.route("/<string:compete_name>/data/download/<string:filename>")
@login_or_role_erquired("member")
def data_download(compete_name, filename):
    upload_dir = current_app.config["MINIO_UPLOAD_DATA_PATH"]
    file = storage.connection.get_object(compete_name, f"{upload_dir}/{filename}")
    fileobj = io.BytesIO()
    with zipfile.ZipFile(fileobj, 'w') as zip_file:
        zip_info = zipfile.ZipInfo(filename)
        zip_info.date_time = time.localtime(time.time())[:6]
        zip_info.compress_type = zipfile.ZIP_DEFLATED
        zip_file.writestr(zip_info, file.data)
    fileobj.seek(0)
    response = make_response(fileobj.read())
    response.headers.set('Content-Type', 'zip')
    response.headers.set('Content-Disposition', 'attachment', filename='%s.zip' % os.path.splitext(os.path.basename(filename))[0])
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
    return redirect(request.url)


@bp_compete.route("/<string:compete_name>/mysubmission")
@login_or_role_erquired("member")
def mysubmission(compete_name):
    print(compete_name)
    return redirect(request.url)


@bp_compete.route("/<string:compete_name>/submission")
@login_or_role_erquired("member")
def submission(compete_name):
    print(compete_name)
    return redirect(request.url)
