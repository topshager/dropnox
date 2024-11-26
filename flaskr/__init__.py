import os
from flask import Flask

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Set default config
    app.config.from_mapping(
        SECRET_KEY='dev',  # For development, use a better secret key in production
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # If test_config is provided, override the default config
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Create the instance folder if it doesn't exist
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Import and initialize the database
    from . import db
    db.init_app(app)

    # Register blueprints
    from . import auth
    app.register_blueprint(auth.bp)

    from . import home
    app.register_blueprint(home.bp)
    app.add_url_rule('/', endpoint='home')

    from . import create
    app.register_blueprint(create.bp)

    from . import folder
    app.register_blueprint(folder.bp)
    app.add_url_rule('/folder', endpoint='folder')
    return app
