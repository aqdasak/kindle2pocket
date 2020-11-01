from flask import Flask

# from config.config import params
from .commands import create_tables
from .extensions import db
from .models import User
from .routes.auth import auth
from .routes.main import main


def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    db.init_app(app)
    # mail.init_app(app)
    #
    # @app.context_processor
    # def global_param():
    #     return dict(params=params)

    app.register_blueprint(main)
    app.register_blueprint(auth)

    app.cli.add_command(create_tables)

    return app
