# -*- coding: utf-8 -*-
import os
from flask import Flask

from config import config_dict
from racoon.extensions import register_extensions


# Setup
def create_app(config_key="debug"):
    register_logger()
    app = Flask(__name__)
    print_start_to_logger(app)
    _config = config_dict[config_key]
    app.config.from_object(_config)  # Enabling config initiation
    register_extension(app)
    register_blueprints(app)
    register_cli(app)
    return app


def register_logger():
    """
    > When you want to configure logging for your project, you should do it as soon as possible when the program starts.
    > If app.logger is accessed before logging is configured, it will add a default handler.
    > If possible, configure logging before creating the application object.
    see https://flask.palletsprojects.com/en/1.1.x/logging/
    :return: None
    """
    from logging.config import dictConfig
    from config import BaseConfig

    log_dir = getattr(BaseConfig, "LOG_DIR")
    log_file_path = os.path.join(log_dir, "logdata.log")
    # Creates logs folder if not existent
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    dictConfig(
        {
            "version": 1,
            "formatters": {
                "file": {
                    "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
                }
            },
            "handlers": {
                "file": {
                    "class": "logging.handlers.TimedRotatingFileHandler",
                    "formatter": "file",
                    "filename": log_file_path,
                    "backupCount": 30,  # 1month
                    "when": "D",
                }
            },
            "root": {"level": "INFO", "handlers": ["file"]},
        }
    )
    return None


def register_extension(app):
    """Register extensions"""
    register_extensions(app)
    app.logger.info("register_extension done")
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    # Registering the view and the api blueprints here
    with app.app_context():
        from racoon.view import views
        for k, v in views.items():
            app.register_blueprint(v)
            app.logger.info("blueprint registration: {}".format(k))
    app.logger.info("register_blueprints done")
    return None


def register_cli(app):
    from racoon.clis import bp_cli as cli_blueprint

    app.register_blueprint(cli_blueprint)
    app.logger.info("register_cli_command done")
    return None


def print_start_to_logger(app):
    app.logger.info("########## App start ##########")
