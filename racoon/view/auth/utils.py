# -*- coding: utf-8 -*-
from functools import wraps

from flask import request, current_app, redirect, url_for
from flask_login import current_user

from racoon.models.user import User, Roles


EXEMPT_METHODS = set(["OPTIONS"])


def login_or_role_erquired(role_name=None):
    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if request.method in EXEMPT_METHODS:
                return func(*args, **kwargs)
            elif current_app.config.get("LOGIN_DISABLED"):
                return func(*args, **kwargs)
            elif current_user.is_authenticated:
                if role_name is None:
                    return func(*args, **kwargs)
                else:
                    req_role = Roles.query.filter(Roles.name == role_name).first()
                    if req_role:
                        user = User.query.filter(
                            User.username == current_user.username
                        ).first()
                        if user.roles[0].id <= req_role.id:
                            return func(*args, **kwargs)
                        else:
                            return redirect(
                                url_for("bp_error.unauthorized", _external=True)
                            )
                    else:
                        ValueError("{} is invalid role name.".format(role_name))
            else:
                current_app.login_manager.unauthorized()

        return decorated_view

    return decorator
