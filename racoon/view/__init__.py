# -*- coding: utf-8 -*-
from racoon.view.auth.auth import bp_auth
from racoon.view.compete.compete import bp_compete
from racoon.view.error.custom import bp_error
from racoon.view.home import bp_home


views = {
    "bp_home": bp_home,
    "bp_error": bp_error,
    "bp_auth": bp_auth,
    "bp_compete": bp_compete,
}


# For error handler
from racoon.view.error.general import err_404
from racoon.view.error.general import err_500


errors = {
    404: err_404,
    500: err_500,
}
