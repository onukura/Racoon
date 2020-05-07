import os


class BaseConfig:
    # Root Dir of this app
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    # server configuration
    HOST = "127.0.0.1"
    PORT = 5000
    SECRET_KEY = "fdvsegserw5w45ear569rseruitn6dnc76tw"
    # Directory path for logger
    LOG_DIR = os.path.join(ROOT_DIR, "log")
    # contest specific variables
    ALLOWED_EXTENSIONS = ["csv", "txt", "zip", "gz"]
    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DebugConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"


class DeployConfig(BaseConfig):
    DEBUG = False
    DB_USER = "postgres"
    DB_PASSWORD = "postgres"
    DB_HOST = "localhost"
    DB_PORT = 5432
    DB_NAME = "dslbp"
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
    )
    # SQLAlchemy
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
