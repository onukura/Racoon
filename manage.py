# -*- coding: utf-8 -*-
import os

from flask_script import Manager
from flask_migrate import MigrateCommand

from racoon import create_app
from racoon.commands import commands


try:
    FLASK_CONFIG = os.environ["FLASK_CONFIG"]
except:
    FLASK_CONFIG = "debug"

# Generate Flask App
app = create_app(FLASK_CONFIG)
manager = Manager(app)
manager.add_command("db", MigrateCommand)
for name, command in commands.items():
    manager.add_command(name, command)


if __name__ == "__main__":
    # Import HTTP server module and run API
    manager.run()
