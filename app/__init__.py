from flask import Flask
from app.config import Config
from app.extensions import db, migrate, bootstrap, mail, moment, babel, qrcode, csrf
from app.utils import get_locale
import logging
from logging.handlers import RotatingFileHandler
import os

from flask_babel import lazy_gettext as _l


def create_app(config_obj=Config()):
    app = Flask(__name__)
    app.config.from_object(config_obj)
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    babel.init_app(app, locale_selector=get_locale)
    qrcode.init_app(app)
    csrf.init_app(app)

    app.jinja_env.globals.update(get_locale=get_locale)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.errors import bp as err_bp
    app.register_blueprint(err_bp)

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
