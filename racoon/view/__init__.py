from racoon.view.home import bp_home
from racoon.view.error import bp_error
from racoon.view.auth.auth import bp_auth
from racoon.view.compete.compete import bp_compete


views = {
    "bp_home": bp_home,
    "bp_error": bp_error,
    "bp_auth": bp_auth,
    "bp_compete": bp_compete,
}
