from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap5

login = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap5()
