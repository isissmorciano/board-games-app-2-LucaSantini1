"""Run module for the board games Flask app.

This file is intentionally small: it initializes the DB and runs the app
from the `app` package.
"""
from app import app
from app.db import init_db


if __name__ == '__main__':
    init_db()
    app.run(debug=True)