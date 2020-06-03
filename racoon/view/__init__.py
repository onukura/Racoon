# -*- coding: utf-8 -*-
from racoon.view.auth.routes import bp_auth
from racoon.view.compete.routes import bp_compete
from racoon.view.error.custom import bp_error
from racoon.view.home import bp_home
from racoon.view.user.routes import bp_user


views = {
    "bp_home": bp_home,
    "bp_error": bp_error,
    "bp_auth": bp_auth,
    "bp_compete": bp_compete,
    "bp_user": bp_user,
}


# For error handler
from racoon.view.error.general import err_404
from racoon.view.error.general import err_500


errors = {
    404: err_404,
    500: err_500,
}
