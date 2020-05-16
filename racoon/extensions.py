from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_user import UserManager
from flask_wtf.csrf import CSRFProtect


# create instance
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()


def register_extensions(app):
    """Register extensions"""

    # Flask-SQLAlchemy
    db.init_app(app)

    # Flask-Migrate
    migrate.init_app(app, db)

    # Flask-Login
    login_manager.init_app(app)

    # CSRF protectioin
    csrf.init_app(app)

    if app.config["DEBUG"]:
        pass

    # Setup Flask-User to handle user account related forms
    from racoon.models.user import User

    # Setup Flask-User
    user_manager = UserManager(app, db, User)

    @app.context_processor
    def context_processor():
        return dict(user_manager=user_manager)

    return None
