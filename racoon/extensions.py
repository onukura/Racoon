from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin

# create instance
db = SQLAlchemy()
login_manager = LoginManager()

users = {'foo@bar.tld': {'password': 'secret'}}

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[email]['password']

    return user


def register_extensions(app):
    """Register extensions"""

    # Flask-SQLAlchemy
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Flask-Login
    login_manager.init_app(app)

    if app.config["DEBUG"]:
        pass

    return None
