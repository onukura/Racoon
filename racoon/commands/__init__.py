# -*- coding: utf-8 -*-
from racoon.commands.init_db import InitDbCommand
from racoon.commands.create_user import CreateUserCommand
from racoon.commands.create_dummy import CreateDummyData


commands = {
    "init_db": InitDbCommand,
    "create_user": CreateUserCommand,
    "create_dummy_data": CreateDummyData,
}
