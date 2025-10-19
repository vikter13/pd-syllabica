"""
Initialization flask application
"""
import os
from flask import Flask, render_template, g
from flask_cors import CORS

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('settings.py', silent=False)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    for cfg in app.config:
        if isinstance(app.config[cfg], str):
            app.config[cfg] = app.config[cfg].replace('{instance}', app.instance_path)

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register the database commands
    from app import db
    db.init_app(app)

    # apply the blueprints to the app

    os.environ['BLUEPRINTS_TYPES'] = app.config.get('BLUEPRINTS_TYPES', "domains")

    from app import auth, quiz, phonotext

    app.register_blueprint(auth.bp)
    app.register_blueprint(quiz.BP)
    app.register_blueprint(phonotext.BP)

#     quiz.init_app(app)
    phonotext.init_app(app)

    from app import livedict
    app.register_blueprint(livedict.BP)
    # livedict.init_app(app)

    @app.route('/')
    def show_index():
        """
        index page render
        """
        g.url_prefix = '.'
        return render_template('index.html')

    return app
