"""This file is the view module which contains the lazysensor, where all the good
stuff happens. You will always want to point your applications like Gunicorn
to this file, which will pick up the lazysensor to run their servers.
"""

import os
import sys

from racoon import create_app

try:
    ENV = os.environ["DEBUG"]
except:
    ENV = "debug"

# Generate Flask App
app = create_app(ENV)


if __name__ == "__main__":
    # Import HTTP server module and run API
    from waitress import serve

    host = app.config["HOST"]
    port = app.config["PORT"]
    print(f"start serve host:{host} / port:{port}")
    serve(app, host=host, port=port)
