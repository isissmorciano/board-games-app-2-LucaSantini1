from flask import Flask

app = Flask(__name__)

# Import routes to register endpoints with the app
from . import routes  # noqa: E402,F401
