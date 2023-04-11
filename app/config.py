import os
from dotenv import load_dotenv, dotenv_values

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    MAX_OWNED_QUEUES_PER_USER = 50

    BABEL_DEFAULT_LOCAL = 'en'
    BABEL_TRANSLATION_DIRECTORIES = os.path.join(basedir, "translations")

    SEND_FILE_MAX_AGE_DEFAULT = 0
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'some-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_recycle': 280, 'pool_pre_ping': True}
    SESSION_COOKIE_NAME = "queue_session"
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT') or \
                             'very-important'

    EMAIL_USER = os.environ.get('EMAIL_USER')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

    # Mail Settings
    MAIL_DEFAULT_SENDER = EMAIL_USER
    MAIL_SERVER = "smtp.mail.ru"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = False
    MAIL_USERNAME = EMAIL_USER
    MAIL_PASSWORD = EMAIL_PASSWORD
