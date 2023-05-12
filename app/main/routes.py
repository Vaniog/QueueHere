from flask import render_template, session
from app.main import bp


@bp.route('/', methods=['POST', 'GET'])
@bp.route('/index', methods=['POST', 'GET'])
def index():
    return render_template('main/index.html')


@bp.after_app_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.cache_control.public = True
    response.cache_control.max_age = 0
    session.permanent = True

    return response
