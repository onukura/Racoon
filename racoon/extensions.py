from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_wtf.csrf import CSRFProtect


# create instance
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


def register_extensions(app):
    """Register extensions"""

    # Flask-SQLAlchemy
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Flask-Login
    login_manager.init_app(app)

    # CSRF protectioin
    csrf.init_app(app)

    if app.config["DEBUG"]:
        pass

    return None
