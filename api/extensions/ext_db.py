from flask import Flask

from models.database import db


def init_db(app: Flask):
    db.init_app(app)
