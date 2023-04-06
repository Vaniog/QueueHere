from flask import Blueprint

bp = Blueprint('queue', __name__)

from app.queue import routes
