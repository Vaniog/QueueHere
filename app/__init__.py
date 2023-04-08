from flask import Flask, request, current_app
from flask_babel import gettext as _, lazy_gettext as _l
from app.config import Config
from app.extensions import db, login, migrate, bootstrap, mail, moment, babel
from app.utils import get_locale
import logging
from logging.handlers import RotatingFileHandler
import os


def create_app(config_obj=Config()):
    app = Flask(__name__)
    app.config.from_object(config_obj)
    db.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)

    babel.init_app(app, locale_selector=get_locale, default_locale='ru')
    print(_l("Hello!"))

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.errors import bp as err_bp
    app.register_blueprint(err_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.queue import bp as queue_bp
    app.register_blueprint(queue_bp)

    login.login_view = 'auth.login'

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
