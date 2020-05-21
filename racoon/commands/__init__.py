# -*- coding: utf-8 -*-
from racoon.commands.init_app import InitAppCommand
from racoon.commands.create_user import CreateUserCommand
from racoon.commands.create_dummy import CreateDummyData


commands = {
    "init_app": InitAppCommand,
    "create_user": CreateUserCommand,
    "create_dummy_data": CreateDummyData,
}
