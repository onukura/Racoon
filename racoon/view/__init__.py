from racoon.view.index import bp_index
from racoon.view.auth.auth import bp_auth
from racoon.view.compete import bp_compete

views = {
    "bp_index": bp_index,
    "bp_auth": bp_auth,
    "bp_compete": bp_compete,
}
