import os


class BaseConfig:
    APP_NAME = "Racoon"
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
    # CSRF key
    WTF_CSRF_SECRET_KEY = "sdpg2398hswefwnjoj"
    # Flask-User settings
    USER_APP_NAME = APP_NAME
    USER_ENABLE_CHANGE_PASSWORD = True  # Allow users to change their password
    USER_ENABLE_CHANGE_USERNAME = False  # Allow users to change their username
    USER_ENABLE_CONFIRM_EMAIL = True  # Force users to confirm their email
    USER_ENABLE_FORGOT_PASSWORD = True  # Allow users to reset their passwords
    USER_ENABLE_EMAIL = True  # Register with Email
    USER_ENABLE_REGISTRATION = True  # Allow new users to register
    USER_REQUIRE_RETYPE_PASSWORD = True  # Prompt for `retype password` in:
    USER_ENABLE_USERNAME = False  # Register and Login with username
    USER_AFTER_LOGIN_ENDPOINT = "main.member_page"
    USER_AFTER_LOGOUT_ENDPOINT = "main.home_page"
    USER_EMAIL_SENDER_EMAIL = "admin@admin.org"


class DebugConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"


class DeployConfig(BaseConfig):
    DEBUG = False
    DB_USER = "postgres"
    DB_PASSWORD = "postgres"
    DB_HOST = "postgres"
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
