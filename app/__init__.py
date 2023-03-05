from flask import Flask
from app.config import Config
from .extensions import db, login, migrate
import logging
from logging.handlers import RotatingFileHandler
import os


def create_app(config_obj=Config()):
    app = Flask(__name__)
    app.config.from_object(config_obj)
    db.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.errors import bp as err_bp
    app.register_blueprint(err_bp)

    login.login_view = 'main.login'

    app.app_context().push()

    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.txt', maxBytes=10240, backupCount=10)

        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
        )
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')

    return app


from app.main import routes
from app.errors import handlers
