# -*- coding: utf-8 -*-
import os


class BaseConfig:
    # Root Dir of this app
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    # server configuration
    SECRET_KEY = "fdvsegserw5w45ear569rseruitn6dnc76tw"
    # Directory path for logger
    LOG_DIR = os.path.join(ROOT_DIR, "log")

    # contest specific variables
    ALLOWED_EXTENSIONS = ["csv", "txt", "zip", "gz"]

    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CSRF key
    WTF_CSRF_SECRET_KEY = "sdpg2398hswefwnjoj"

    # Storage
    STORAGE_TYPE = "minio"  # minio or filesystem
    # MINIO (if STORAGE_TYPE == "minio")
    MINIO_ENDPOINT = "minio:9000"
    MINIO_ACCESS_KEY = "minio"
    MINIO_SECRET_KEY = "minio123"
    MINIO_SECURE = False
    # File System (if STORAGE_TYPE == "filesystem")
    STORAGE_FD_DIR = "storage"
    # Storage directory setting
    STORAGE_PATH_ANSWER = "answer"  # path will be {bucket name}:/{STORAGE_PATH_ANSWER} or ./storage/{STORAGE_PATH_ANSWER}
    STORAGE_PATH_DATA = "data"  # path will be /{STORAGE_PATH_DATA}
    STORAGE_PATH_SUBMISSION = "submission"  # path will be /{STORAGE_PATH_SUBMISSION}

    # Submission setting
    FILENAME_ANSWER = "answer.csv"


class DebugConfig(BaseConfig):
    DEBUG = True
    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"


class DeployConfig(BaseConfig):
    DEBUG = False
    # DB
    DB_USER = "postgres"
    DB_PASSWORD = "postgres"
    DB_HOST = "postgresql"
    DB_PORT = "5432"
    DB_NAME = "racoon"
    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 120,
        "pool_timeout": 900,
        "pool_size": 30,
        "max_overflow": 30,
    }
    SQLALCHEMY_RECORD_QUERIES = True


# Create a config dictionary which is used while initiating the application.
config_dict = {
    "common": BaseConfig,
    "debug": DebugConfig,
    "deploy": DeployConfig,
}
