import flask_migrate
from flask import Flask

from models.database import db


def init_migrate(app: Flask):
    flask_migrate.Migrate(app, db)
