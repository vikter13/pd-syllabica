'''
 Main database module
'''
import click
from flask import current_app, g
import flask_migrate
from flask.cli import with_appcontext

import app.mod.models as models

PDB = models.db

def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if 'db' not in g:
        g.db = models

    return g.db


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    PDB.init_app(app)
    app.MIGRATE = flask_migrate.Migrate(app, PDB)
