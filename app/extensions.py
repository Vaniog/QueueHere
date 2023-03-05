from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

login = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
