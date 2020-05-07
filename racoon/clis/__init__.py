from flask import Blueprint, current_app
from flask.cli import with_appcontext

from racoon.extensions import db


bp_cli = Blueprint("utils", __name__)


@bp_cli.cli.command("hello")
def hello():
    """say hello for testing"""
    current_app.logger.info("cli: Hello Flask!!")
    return None


@bp_cli.cli.command("initialize_db")
@with_appcontext
def recreate_db():
    """
    Recreates a local database. You probably should not use this on
    production.
    """
    current_app.logger.info("cli: start recreate_db.")
    db.drop_all()
    current_app.logger.info("cli: dropped all tables.")
    db.create_all()
    current_app.logger.info("cli: recreated all tables.")
    db.session.commit()
    current_app.logger.info("cli: recreate_db done")
    print("Database initialized.")
    return None
